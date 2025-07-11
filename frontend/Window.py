import json
from PySide6.QtGui import QMouseEvent, QGuiApplication, QAction
from PySide6.QtCore import Qt, QPropertyAnimation, Signal
from PySide6.QtWidgets import QMessageBox, QDialog

from frontend.LoginWindow import LoginWindow
from gui.ui.utils.customGrips import CustomGrip
from frontend.ShowWindow import SHOWWINDOW


class MainWindow(SHOWWINDOW):
    closed = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.center()
        # --- 拖动窗口 改变窗口大小 --- #
        self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
        self.right_grip = CustomGrip(self, Qt.RightEdge, True)
        self.top_grip = CustomGrip(self, Qt.TopEdge, True)
        self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)
        self.setAcceptDrops(True)  # ==> 设置窗口支持拖动（必须设置）
        # --- 拖动窗口 改变窗口大小 --- #
        self.animation_window = None

        # 退出登录
        self.ui.log_out_button.clicked.connect(self.logout)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.mouse_start_pt = event.globalPosition().toPoint()
            self.window_pos = self.frameGeometry().topLeft()
            self.drag = True

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.drag:
            distance = event.globalPosition().toPoint() - self.mouse_start_pt
            self.move(self.window_pos + distance)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.drag = False

    def center(self):
        screen = QGuiApplication.primaryScreen().size()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2 - 10)

    # 拖动窗口 改变窗口大小
    def resizeEvent(self, event):
        # Update Size Grips
        self.resizeGrip()

    def showEvent(self, event):
        super().showEvent(event)
        if not event.spontaneous():
            # 定义显示动画
            self.animation = QPropertyAnimation(self, b"windowOpacity")
            self.animation.setDuration(500)  # 动画时间500毫秒
            self.animation.setStartValue(0)  # 从完全透明开始
            self.animation.setEndValue(1)  # 到完全不透明结束
            self.animation.start()

    def closeEvent(self, event):
        if not self.animation_window:
            config = dict()
            config['iou'] = self.ui.iou_spinbox.value()
            config['conf'] = self.ui.conf_spinbox.value()
            config_json = json.dumps(config, ensure_ascii=False, indent=2)
            with open('data/config/setting.json', 'w', encoding='utf-8') as f:
                f.write(config_json)
            self.stopDetect()
            self.animation_window = QPropertyAnimation(self, b"windowOpacity")
            self.animation_window.setStartValue(1)
            self.animation_window.setEndValue(0)
            self.animation_window.setDuration(500)
            self.animation_window.start()
            self.animation_window.finished.connect(self.close)
            event.ignore()
        else:
            self.setWindowOpacity(1.0)
            self.closed.emit()

    def logout(self):
        reply = QMessageBox.question(
            self, "确认退出", "确定要退出登录吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.stopDetect()
            self.close()  # 关闭当前主窗口

            # 再次显示登录窗口
            login_window = LoginWindow()
            if login_window.exec() == QDialog.Accepted:
                new_main_window = MainWindow()
                new_main_window.show()

                # 更新 glo 中的主窗口引用
                from frontend.utils import glo
                glo.set_value('main_window', new_main_window)
