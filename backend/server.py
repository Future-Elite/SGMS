import atexit
import base64
import datetime

import numpy as np
from flask import Flask, request, jsonify, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from data.models import GestureMap, DeviceTypeEnum, ResultEnum, User
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from celery_worker import async_commit_log
import jwt
import cv2

# 创建 Flask 应用
flask_app = Flask(__name__)
SECRET_KEY = 'SGMS_Secret_Key'

# 创建数据库引擎和会话
engine = create_engine('sqlite:///data/database.db', echo=False)
SessionLocal = scoped_session(sessionmaker(bind=engine))
gesture_name = None
username = None
token = None
gesture_labels = {
    'Left_Double_Click': 0,
    'backward': 1,
    'forward': 2,
    'high': 3,
    'left_click': 4,
    'low': 5,
    'mouse': 6,
    'activate': 7,
    'right_click': 8,
    'start_or_pause': 9
}

camera = cv2.VideoCapture(0)


@atexit.register
def cleanup_camera():
    if camera.isOpened():
        camera.release()


def load_gesture_map_dict():
    session = SessionLocal()
    try:
        gestures = session.query(GestureMap).all()
        return {g.gesture_name: {"id": gesture_labels[g.gesture_name],
                                 "operation_type": g.operation_type.value} for g in gestures}
    finally:
        session.close()


gesture_map_dict = load_gesture_map_dict()


# 后台异步写日志
def async_commit(log_entry):
    s = SessionLocal()
    try:
        s.add(log_entry)
        s.commit()
    except Exception as e:
        print("DB Commit Error:", e)
        s.rollback()
    finally:
        s.close()


# 视频流接口
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# Token 验证接口
@flask_app.route('/api/auth', methods=['POST'])
def auth():
    global username, token
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing token"}), 400

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        return jsonify({"message": f"验证成功，欢迎用户：{username}"}), 200
    except ExpiredSignatureError:
        return jsonify({"error": "Token 已过期"}), 401
    except InvalidTokenError:
        return jsonify({"error": "无效的 Token"}), 403


# Token 刷新接口
@flask_app.route('/api/refresh', methods=['POST'])
def refresh_token():
    global token
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing token"}), 400

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        exp = payload.get("exp")
        now = datetime.datetime.now().timestamp()

        if now > exp:
            return jsonify({"error": "Token 已过期，无法刷新"}), 401

        # 生成新 token
        new_payload = {
            "username": payload["username"],
            "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
        }
        new_token = jwt.encode(new_payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": new_token}), 200

    except InvalidTokenError:
        return jsonify({"error": "无效的 Token"}), 403


@flask_app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@flask_app.route('/result', methods=['POST'])
def upload_result():
    global gesture_name
    session = SessionLocal()
    try:
        data = request.get_json()
        gesture_name = list(data.keys())[0].strip() if data else None
        user = session.query(User).filter_by(username=username).first()

        if not gesture_name or gesture_name not in gesture_map_dict:
            return jsonify({"error": "未知或未注册的手势"}), 400

        gesture_info = gesture_map_dict[gesture_name]

        log_data = {
            "user_id": user.id,
            "gesture_id": gesture_info['id'],
            "operation_type": gesture_info['operation_type'],
            "device_type": DeviceTypeEnum.tv.name,
            "result": ResultEnum.success.name,
            "detail": f"检测到手势：{gesture_name}"
        }
        print(log_data)
        # 异步提交日志
        async_commit_log.delay(log_data)

        return jsonify({"message": f"手势“{gesture_name}”记录成功"}), 200

    except Exception as e:
        session.rollback()
        print(f"Server error: {e}")
        print(username)
        return jsonify({"error": "服务端异常"}), 500
    finally:
        session.close()


def recognize_gesture_from_frame(frame):
    import mediapipe as mp
    from ultralytics import YOLO
    labels = {
        0: 'Left_Double_Click',
        1: 'backward',
        2: 'forward',
        3: 'high',
        4: 'left_click',
        5: 'low',
        6: 'mouse',
        7: 'activate',
        8: 'right_click',
        9: 'start_or_pause'
    }
    black_img = np.zeros(frame.shape, dtype=np.uint8)
    mp_pose = mp.solutions.hands
    hands = mp_pose.Hands(True, 1, 1, 0.5, 0.5)
    results = hands.process(frame)
    if results.multi_hand_landmarks:
        for oneHand in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                black_img, oneHand, mp.solutions.hands.HAND_CONNECTIONS,
            )
    model = YOLO('cv_module/ptfiles/yolo11s-cls.pt')
    res = model.predict(black_img)
    gesture_id = res[0].probs.top1
    confidence = res[0].probs.top1conf.item()
    return labels[gesture_id], confidence


@flask_app.route('/api/recognize', methods=['POST'])
def recognize_gesture():
    global username, token
    data = request.get_json()

    if not token:
        return jsonify({"error": "缺少 token"}), 401

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        if not username:
            return jsonify({"error": "无效用户"}), 403
    except ExpiredSignatureError:
        return jsonify({"error": "Token 已过期"}), 401
    except InvalidTokenError:
        return jsonify({"error": "无效 Token"}), 403

    frame_data = data.get("frame_data")
    session_id = data.get("session_id")

    if not frame_data or not session_id:
        return jsonify({"status": "error", "message": "缺少必要字段"}), 400

    try:
        # 解码 base64 图像
        img_bytes = base64.b64decode(frame_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"status": "error", "message": "图像解码失败"}), 400

        # 手势识别
        gesture, confidence = recognize_gesture_from_frame(frame)

        return jsonify({
            "status": "success",
            "gesture": gesture,
            "confidence": round(confidence, 2)
        }), 200

    except Exception as e:
        print("识别失败:", e)
        return jsonify({"status": "error", "message": "服务端异常"}), 500


@flask_app.route('/result', methods=['GET'])
def get_result():
    return jsonify(gesture_name), 200


@flask_app.route('/')
def index():
    return "Flask服务已启动"


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000, debug=False)
