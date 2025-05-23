from flask import Flask, request, jsonify, Response
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import cv2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import GestureMap, OperationLog, DeviceTypeEnum, ResultEnum

flask_app = Flask(__name__)
SECRET_KEY = 'SGMS_Secret_Key'
gesture_name = None
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
        # 读取视频帧
        success, frame = camera.read()
        if not success:
            break
        else:
            # 编码为 JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # 生成多部分响应
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@flask_app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# 上传检测结果接口（JSON 方式）
@flask_app.route('/result', methods=['POST'])
def upload_result():
    global gesture_name
    data = request.get_json()

    gesture_labels = {
        'Left_Double_Click': 0,
        'backward': 1,
        'forward': 2,
        'high': 3,
        'left_click': 4,
        'low': 5,
        'mouse': 6,
        'pause': 7,
        'right_click': 8,
        'start': 9
    }

    session = SessionLocal()
    try:
        gesture_name = list(data.keys())[0] if data else None
        gesture_name = gesture_name.strip() if gesture_name else None

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
        print(f"Server error: {e}")
        return jsonify({"error": "服务端异常"}), 500
    finally:
        session.close()


@flask_app.route('/result', methods=['GET'])
def get_result():
    return jsonify(gesture_name), 200


@flask_app.route('/')
def index():
    return "Flask服务已启动"


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000)
