import jwt
import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)
from frontend.api import send_jwt_to_server

SECRET_KEY = 'your_secret_key_here'
USER_DB = {"admin": "123456"}  # 模拟数据库


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户登录")
        self.setFixedSize(300, 250)

        self.is_login_mode = True

        self.layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("用户名")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("确认密码（注册）")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.confirm_input)
        self.confirm_input.hide()

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        self.action_button = QPushButton("登录")
        self.action_button.clicked.connect(self.handle_action)
        self.layout.addWidget(self.action_button)

        self.switch_button = QPushButton("没有账号？点击注册")
        self.switch_button.clicked.connect(self.switch_mode)
        self.layout.addWidget(self.switch_button)

        self.setLayout(self.layout)

    def switch_mode(self):
        self.is_login_mode = not self.is_login_mode
        if self.is_login_mode:
            self.setWindowTitle("用户登录")
            self.confirm_input.hide()
            self.action_button.setText("登录")
            self.switch_button.setText("没有账号？点击注册")
        else:
            self.setWindowTitle("用户注册")
            self.confirm_input.show()
            self.action_button.setText("注册")
            self.switch_button.setText("已有账号？点击登录")
        self.status_label.setText("")

    def handle_action(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.status_label.setText("请输入用户名和密码")
            return

        if self.is_login_mode:
            if USER_DB.get(username) == password:
                token = self.generate_jwt(username)
                status, resp = send_jwt_to_server(token)
                QMessageBox.information(self, "登录成功", f"JWT:\n{token}\n服务器响应: {resp}")
                self.accept()
            else:
                self.status_label.setText("用户名或密码错误")
        else:
            confirm = self.confirm_input.text().strip()
            if password != confirm:
                self.status_label.setText("两次密码不一致")
                return
            if username in USER_DB:
                self.status_label.setText("用户名已存在")
                return
            USER_DB[username] = password
            QMessageBox.information(self, "注册成功", "请登录")
            self.switch_mode()

    def generate_jwt(self, username):
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
