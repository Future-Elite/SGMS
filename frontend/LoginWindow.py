import datetime

import jwt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.models import User
from frontend.api import send_jwt_to_server

engine = create_engine("sqlite:///data/database.db")
Session = sessionmaker(bind=engine)
SECRET_KEY = 'SGMS_Secret_Key'


def generate_jwt(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户登录")
        self.setFixedSize(350, 300)

        self.is_login_mode = True

        # 主布局
        self.layout = QVBoxLayout()

        # 用户名输入框
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("用户名")
        self.layout.addWidget(self.username_input)

        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        # 确认密码输入框（仅在注册模式下显示）
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("确认密码（注册）")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.confirm_input)
        self.confirm_input.hide()

        # 登录/注册按钮
        self.action_button = QPushButton("登录")
        self.action_button.clicked.connect(self.handle_action)
        self.layout.addWidget(self.action_button)

        # 切换按钮
        self.switch_button = QPushButton("没有账号？点击注册")
        self.switch_button.clicked.connect(self.switch_mode)
        self.layout.addWidget(self.switch_button)

        # 显示信息的区域（放在最下方）
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 6pt; color: green;")  # 修改字体大小和颜色
        self.status_label.setStyleSheet("border: 1px solid black; padding: 5px;")
        self.layout.addWidget(self.status_label)

        # 设置布局
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

        session = Session()

        if self.is_login_mode:
            user = session.query(User).filter_by(username=username).first()
            if user and user.password == password:
                token = generate_jwt(username)
                status, resp = send_jwt_to_server(token)
                if not status:
                    self.status_label.setText(f"登录失败: {resp}")
                    return
                self.accept()
            else:
                self.status_label.setText("用户名或密码错误")
                self.password_input.clear()
        else:
            if session.query(User).filter_by(username=username).first():
                self.status_label.setText("用户名已存在")
            else:
                new_user = User(username=username, password=password)
                session.add(new_user)
                session.commit()
                self.status_label.setText("注册成功，请登录！")
                self.switch_mode()

        session.close()
