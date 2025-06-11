import datetime

import jwt
import requests
from PySide6.QtCore import Qt, QTimer
from frontend.utils.hash import generate_salt, hash_password, verify_password
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QFrame
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.models import User
from frontend.utils import glo

engine = create_engine("sqlite:///data/database.db", echo=False)
Session = sessionmaker(bind=engine)
SECRET_KEY = 'SGMS_Secret_Key'


def generate_jwt(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def send_jwt_to_server(jwt_token: str):
    try:
        response = requests.post("http://127.0.0.1:5000/api/auth", json={"token": jwt_token})
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}


def refresh_token(token):
    try:
        response = requests.post("http://127.0.0.1:5000/api/refresh", json={"token": token})
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}


def input_style():
    return """
        QLineEdit {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-color: #4CAF50;
        }
    """


def button_style(color, hover_color):
    return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
    """


def title_button_style():
    return """
        QPushButton {
            background-color: #444;
            color: white;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #666;
        }
    """


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.timer = None
        self.setAttribute(Qt.WA_TranslucentBackground)  # 圆角支持
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setFixedSize(500, 480)

        self._try_times = 0
        self.is_login_mode = True
        self.old_pos = self.pos()

        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # 卡片背景
        self.card = QFrame()
        self.card.setStyleSheet("""
                    QFrame {
                        background-color: #ffffff;
                        border-radius: 15px;
                        border: 1px solid #ccc;
                    }
                """)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(20, 10, 20, 20)
        self.main_layout.addWidget(self.card)

        # ========== 登录标题 + 最小化/关闭按钮 ==========
        top_bar = QHBoxLayout()
        title_label = QLabel("🔐 SGMS 系统")
        title_label.setStyleSheet("font-size: 16px;"
                                  "border: none;")
        top_bar.addWidget(title_label)
        top_bar.addStretch()

        minimize_btn = QPushButton("—")
        minimize_btn.setFixedSize(24, 24)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #ddd;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        close_btn.clicked.connect(self.close)

        top_bar.addWidget(minimize_btn)
        top_bar.addWidget(close_btn)

        self.card_layout.addLayout(top_bar)

        # 图标
        self.icon_label = QLabel("🔐")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 28px;")
        self.card_layout.addWidget(self.icon_label)

        # 用户名输入框
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("用户名")
        self.username_input.setStyleSheet(input_style())
        self.username_input.setFixedHeight(40)
        self.card_layout.addWidget(self.username_input)

        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style())
        self.password_input.setFixedHeight(40)
        self.card_layout.addWidget(self.password_input)

        # 确认密码输入框（注册时显示）
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("确认密码（注册）")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setStyleSheet(input_style())
        self.confirm_input.setFixedHeight(40)
        self.confirm_input.hide()
        self.card_layout.addWidget(self.confirm_input)

        # 登录或注册按钮
        self.action_button = QPushButton("登录")
        self.action_button.setFixedHeight(40)
        self.action_button.setStyleSheet(button_style("#4CAF50", "#45a049"))
        self.action_button.clicked.connect(self.handle_action)
        self.card_layout.addWidget(self.action_button)
        self.action_button.setShortcut("Return")

        # 切换按钮
        self.switch_button = QPushButton("没有账号？点击注册")
        self.switch_button.setFixedHeight(35)
        self.switch_button.setStyleSheet(button_style("#2196F3", "#1976D2"))
        self.switch_button.clicked.connect(self.switch_mode)
        self.card_layout.addWidget(self.switch_button)

        # 状态栏
        self.status_label = QTextEdit()
        self.status_label.setReadOnly(True)
        self.status_label.setStyleSheet("""
            QTextEdit {
                font: 10pt "Segoe UI";
                color: rgba(0, 0, 0, 180);
                background-color: #fafafa;
                border-radius: 8px;
                padding: 8px;
                border: 1px solid #ccc;
            }
        """)
        self.status_label.setMinimumHeight(80)
        self.card_layout.addWidget(self.status_label)

        # 初始提示
        self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | Flask Running on http://127.0.0.1:5000")

        self.token_timer = QTimer(self)
        self.token_timer.timeout.connect(self.check_and_refresh_token)
        self.token_timer.start(5 * 60 * 1000)  # 每5分钟检查一次

    def check_and_refresh_token(self):
        token = glo.get_value('token')
        if not token:
            return False

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
            exp_timestamp = payload['exp']
            remaining_time = exp_timestamp - datetime.datetime.now().timestamp()

            # 如果剩余小于5分钟则尝试刷新
            if remaining_time < 300:
                status, new_token = refresh_token(token)
                if status == 200:
                    glo.set_value('token', new_token['token'])
                    self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | JWT 已刷新")
                else:
                    self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | JWT 刷新失败")
                    return False
            return True
        except jwt.ExpiredSignatureError:
            self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | Token 已过期，请重新登录")
            return False
        except jwt.InvalidTokenError:
            self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | Token 无效")
            return False

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

        status = "登录中" if self.is_login_mode else "注册中"
        self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" | {status}")

    def handle_action(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | 用户名或密码不能为空")
            return

        session = Session()

        try:
            if self.is_login_mode:
                user = session.query(User).filter_by(username=username).first()
                if user and verify_password(user.password_hash, user.password_salt, password):
                    token = generate_jwt(username)
                    status, resp = send_jwt_to_server(token)
                    glo.set_value('resp', resp)
                    glo.set_value('token', token)
                    if not status:
                        self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | JWT 发送失败")
                        return
                    if status != 200:
                        self.update_info(
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | Flask 返回错误:" + str(resp))
                        return
                    glo.set_value('user', username)
                    self.accept()
                else:
                    self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | 用户名或密码错误")
                    self.password_input.clear()
                    self._try_times += 1
            else:
                if session.query(User).filter_by(username=username).first():
                    self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | 用户名已存在")
                else:
                    salt = generate_salt()
                    password_hash_val = hash_password(password, salt)
                    new_user = User(username=username, password_salt=salt, password_hash=password_hash_val)
                    session.add(new_user)
                    session.commit()
                    self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | 注册成功")
                    self.switch_mode()
        except Exception as e:
            self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" | 服务器错误: {str(e)}")
        finally:
            session.close()

        if self._try_times >= 3:
            self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | 尝试次数过多，请稍后再试")
            self.action_button.setEnabled(False)
            # 设置定时器，5秒后重新启用按钮
            self.timer = QTimer(self)
            self.timer.start(5000)
            self.timer.timeout.connect(self.enable_button)
            self._try_times = 0

    def enable_button(self):
        self.update_info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | 请重新登录")
        self.action_button.setEnabled(True)
        self.timer.stop()
        self.timer.deleteLater()


    def update_info(self, message):
        self.status_label.append(message)
        self.status_label.verticalScrollBar().setValue(
            self.status_label.verticalScrollBar().maximum()
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()
