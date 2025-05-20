import atexit
import logging
import os
import subprocess
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QDialog

from frontend.LoginWindow import LoginWindow
from frontend.Window import MainWindow
from frontend.utils import glo


# 启动 Flask 后端
flask_process = subprocess.Popen(
    [sys.executable, 'backend/server.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)


def cleanup():
    flask_process.terminate()
    flask_process.wait()


atexit.register(cleanup)

# 添加路径
sys.path.append(os.path.join(os.getcwd(), "gui/ui"))

# 禁用日志
logging.disable(logging.CRITICAL)
# sys.stdout = open(os.devnull, 'w')


if __name__ == '__main__':

    app = QApplication([])
    app.setWindowIcon(QIcon('gui/images/icon.ico'))
    app.setStyleSheet("QFrame { border: none; }")

    login_window = LoginWindow()

    if login_window.exec() == QDialog.Accepted:

        main_window = MainWindow()
        glo.init()
        glo.set_value('main_window', main_window)
        main_window.show()
        app.exec()
    else:
        sys.exit()
