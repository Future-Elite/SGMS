from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QImage
import cv2


class FloatingWindow(QWidget):
    def __init__(self, get_send_out_func):
        super().__init__()
        self.get_send_out = get_send_out_func

        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint | # 始终最前
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明

        # 图像显示标签
        self.label = QLabel(self)
        self.label.setFixedSize(480, 360)
        self.label.setStyleSheet("background-color: black;")
        self.label.setAlignment(Qt.AlignCenter)

        # 关闭按钮
        self.close_button = QPushButton("×", self.label)  # 以 label 为父控件，悬浮其上
        self.close_button.setFixedSize(24, 24)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 180);
                color: white;
                border-radius: 12px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 230);
            }
        """)
        self.close_button.clicked.connect(self.close)

        self.close_button.move(self.label.width() - self.close_button.width() - 5, 5)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)

        # 定时器更新画面
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(30)

        self.move(0, 0)

    def update_image(self):
        frame = self.get_send_out()
        if frame is not None:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image).scaled(self.label.size(), Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()
