import logging
import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from utils import glo
from frontend.Window import MainWindow

# 将ui目录添加到系统路径中
sys.path.append(os.path.join(os.getcwd(), "ui"))

# 禁止标准输出
logging.disable(logging.CRITICAL)  # 禁用所有级别的日志
sys.stdout = open(os.devnull, 'w')  # 禁用标准输出


if __name__ == '__main__':
    app = QApplication([])  # 创建应用程序实例
    app.setWindowIcon(QIcon('gui/images/icon.ico'))  # 设置应用程序图标

    # 为整个应用程序设置样式表，去除所有QFrame的边框
    app.setStyleSheet("QFrame { border: none; }")

    # 创建主窗口
    main_window = MainWindow()

    # 初始化全局变量管理器，并设置值
    glo._init()  # 初始化全局变量空间
    glo.set_value('main_window', main_window)  # 存储窗口实例

    # 从全局变量管理器中获取窗口实例
    glo.get_value('main_window').show()

    app.exec()  # 启动应用程序的事件循环
