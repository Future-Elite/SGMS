from flask import Flask, request, jsonify
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

flask_app = Flask(__name__)
SECRET_KEY = 'your_secret_key_here'


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


@flask_app.route('/')
def index():
    return "JWT验证服务已启动"
