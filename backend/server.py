from flask import Flask, request, jsonify, Response
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import cv2

flask_app = Flask(__name__)
SECRET_KEY = 'SGMS_Secret_Key'


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
    print("接收到检测结果:", data)

    # 假设数据格式：{"objects": [{"label": "person", "confidence": 0.98}, ...]}
    return jsonify({"message": "检测结果上传成功"}), 200


@flask_app.route('/')
def index():
    return "Flask 实时视频流和检测上传服务已启动"


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000)
