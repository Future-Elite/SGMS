import os
import time

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon

from cv_module.CVThread import CVThread
from frontend.BaseWindow import BASEWINDOW
from frontend.utils.ThreadPool import ThreadPool
from gui.ui.UI import Ui_MainWindow
from PySide6.QtWidgets import QGraphicsDropShadowEffect
import psutil
from PySide6.QtCore import QTimer


def applyShadow(widget, color=QColor(0, 0, 0, 80), blur=16):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setColor(color)
    shadow.setOffset(0, 0)
    widget.setGraphicsEffect(shadow)


def getSystemLatency():
    start = time.perf_counter()
    time.sleep(0.001)  # 模拟 I/O 等待
    end = time.perf_counter()
    return (end - start) * 1000  # 转换为毫秒


class SHOWWINDOW(BASEWINDOW):
    def __init__(self):
        super().__init__()
        self.perf_timer = None
        self.is_playing = False
        self.current_model = None
        self.current_workpath = os.getcwd()
        self.inputPath = 0
        self.result_statistic = None
        self.detect_result = None

        # --- 加载UI --- #
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 透明背景
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无头窗口
        self.initSiderWidget()
        # --- 加载UI --- #

        # --- 最大化 最小化 关闭 --- #
        self.ui.maximizeButton.clicked.connect(self.float_window)
        self.ui.minimizeButton.clicked.connect(self.showMinimized)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.topbox.doubleClickFrame.connect(self.float_window)
        # --- 最大化 最小化 关闭 --- #

        # --- 播放 暂停 停止 --- #
        self.ui.run_button.setIcon(QIcon(f"{self.current_workpath}/gui/images/play.png"))
        # --- 播放 暂停 停止 --- #

        self.ui.src_database.clicked.connect(self.showTableResult)
        self.ui.src_database.setIcon(QIcon(f"{self.current_workpath}/gui/images/table.png"))
        self.ui.src_database.setIconSize(self.ui.src_database.size())
        self.ui.src_database.setStyleSheet("""
            QPushButton {
                text-align: center;
                qproperty-iconSize: 30px 30px;
                border: none;
                background-color: transparent;
            }
        """)

        # --- 状态栏 初始化 --- #
        self.shadowStyle(self.ui.mainBody, QColor(0, 0, 0, 38), top_bottom=['top', 'bottom'])
        # --- 状态栏 初始化 --- #

        self.initThreads()

        # --- 超参数调整 --- #
        self.ui.iou_spinbox.valueChanged.connect(lambda x: self.changeValue(x, 'iou_spinbox'))
        self.ui.iou_slider.valueChanged.connect(lambda x: self.changeValue(x, 'iou_slider'))
        self.ui.conf_spinbox.valueChanged.connect(lambda x: self.changeValue(x, 'conf_spinbox'))
        self.ui.conf_slider.valueChanged.connect(lambda x: self.changeValue(x, 'conf_slider'))
        # --- 超参数调整 --- #

        # --- 开始 / 停止 --- #
        self.ui.run_button.clicked.connect(self.runorContinue)
        self.ui.stop_button.clicked.connect(self.stopDetect)
        # --- 开始 / 停止 --- #

        # --- Setting栏 初始化 --- #
        self.loadConfig()
        # --- Setting栏 初始化 --- #

        self.ui.status.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 13px;
            }
        """)

        self.initPerformanceMonitor()

        self.showStatus("多场景手势智能交互控制系统已启动")
        self.setUIStyle()

    def setUIStyle(self):
        self.ui.run_button.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background-color: #2ecc71;
                }
            """)
        self.ui.stop_button.setStyleSheet("""
                QPushButton {
                    background-color: #c0392b;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background-color: #e74c3c;
                }
            """)

        self.ui.stop_button.setIcon(QIcon(f"{self.current_workpath}/gui/images/stop.png"))

        # 添加阴影
        applyShadow(self.ui.run_button)
        applyShadow(self.ui.stop_button)

    def initThreads(self):
        self.yolo_threads = ThreadPool()
        self.yolo_threads.set('yolov11', CVThread())
        self.initModel(yoloname='yolov11')

    def initPerformanceMonitor(self):
        self.perf_timer = QTimer(self)
        self.perf_timer.timeout.connect(self.updateSystemStatus)
        self.perf_timer.start(2000)  # 每 2 秒更新一次

    def updateSystemStatus(self):
        cpu = psutil.cpu_percent()
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        mem_rss_mb = mem_info.rss / 1024 / 1024  # 以 MB 显示常驻内存（RSS）
        delay = getSystemLatency()
        status_msg = f"CPU: {cpu:.1f}%\n内存: {mem_rss_mb:.1f} MB\n系统延迟: {delay:.1f} ms"
        self.ui.status.setText(status_msg)

    def runModelProcess(self, yolo_name):
        yolo_thread = self.yolo_threads.get(yolo_name)
        yolo_thread.source = self.inputPath
        yolo_thread.stop_dtc = False
        if self.ui.run_button.isChecked():
            yolo_thread.is_continue = True
            self.yolo_threads.start_thread(yolo_name)
        else:
            yolo_thread.is_continue = False
            self.showStatus('Pause Detection')

    def runModel(self, runbuttonStatus=None):
        if runbuttonStatus:
            self.ui.run_button.setChecked(True)
        self.runModelProcess('yolov11')

    # 开始/暂停 预测
    def runorContinue(self):
        if not self.is_controling:
            self.start_control()

        if self.inputPath is not None:
            self.is_playing = not self.is_playing
            icon_path = "gui/images/pause.png" if self.is_playing else "gui/images/play.png"
            self.ui.run_button.setIcon(QIcon())
            self.ui.run_button.setIcon(QIcon(icon_path))
            if self.is_playing:
                self.ui.run_button.setStyleSheet("""
                    QPushButton {
                        background-color: #f1c40f;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 6px 12px;
                    }
                    QPushButton:hover {
                        background-color: #f39c12;
                    }
                """)
            else:
                self.ui.run_button.setStyleSheet("""
                                QPushButton {
                                    background-color: #27ae60;
                                    color: white;
                                    border: none;
                                    border-radius: 8px;
                                    padding: 6px 12px;
                                }
                                QPushButton:hover {
                                    background-color: #2ecc71;
                                }
                            """)
            self.runModel()
        else:
            self.showStatus("Please select Camera before starting detection")
            self.ui.run_button.setChecked(False)

    # 停止识别
    def stopDetect(self):
        self.ui.run_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: #27ae60;
                                            color: white;
                                            border: none;
                                            border-radius: 8px;
                                            padding: 6px 12px;
                                        }
                                        QPushButton:hover {
                                            background-color: #2ecc71;
                                        }
                                    """)
        if self.is_controling:
            self.stop_control()
        self.quitRunningModel(stop_status=True)
        self.is_playing = False
        self.ui.run_button.setChecked(False)
        self.ui.run_button.setIcon(QIcon(
            f"{self.current_workpath}/gui/images/play.png"))
        self.ui.main_rightbox.clear()
