from flask import Flask, request, jsonify, Response
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import cv2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.models import GestureMap, OperationLog, DeviceTypeEnum, ResultEnum

flask_app = Flask(__name__)
SECRET_KEY = 'SGMS_Secret_Key'

# 创建数据库引擎和会话
engine = create_engine('sqlite:///data/database.db', echo=False)
SessionLocal = sessionmaker(bind=engine)

camera = cv2.VideoCapture(0)


# Token 验证接口
@flask_app.route('/api/auth', methods=['POST'])
def auth():
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


# 视频流接口
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # 编码为 JPEG 格式
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            # 使用 multipart 返回视频流
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@flask_app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# 上传检测结果接口（JSON 方式）
@flask_app.route('/result', methods=['POST'])
def upload_result():
    data = request.get_json()

    gesture_labels = {
        "start": 0,
        "pause": 1,
        "forward": 2,
        "backward": 3,
        "high": 4,
        "low": 5
    }

    session = SessionLocal()
    try:
        gesture_name = list(data.keys())[0] if data else None
        gesture_name = gesture_name.strip() if gesture_name else None
        print("检测到的手势:", gesture_name)

        if not gesture_name:
            return jsonify({"error": "未知手势"}), 400

        # 查找 gesture_id 和操作类型
        gesture = session.query(GestureMap).filter_by(gesture_name=gesture_name).first()
        if not gesture:
            return jsonify({"error": "手势未注册"}), 404

        # 写入 operation_log
        log = OperationLog(
            gesture_id=gesture_labels[gesture_name],
            operation_type=gesture.operation_type,
            device_type=DeviceTypeEnum.tv,
            result=ResultEnum.success,
            detail=f"检测到手势：{gesture_name}"
        )
        session.add(log)
        session.commit()


        return jsonify({"message": f"手势“{gesture_name}”记录成功"}), 200
    except Exception as e:
        session.rollback()
        print("数据库写入出错:", e)
        return jsonify({"error": "服务端异常"}), 500
    finally:
        session.close()


@flask_app.route('/')
def index():
    return "Flask 实时视频流和检测上传服务已启动"


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000)
