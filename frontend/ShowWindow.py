import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QMainWindow

from frontend.BaseWindow import BASEWINDOW, MODEL_THREAD_CLASSES
from frontend.utils.ThreadPool import ThreadPool
from gui.ui.UI import Ui_MainWindow
from frontend.utils import glo

GLOBAL_WINDOW_STATE = True
WIDTH_LEFT_BOX_STANDARD = 120
WIDTH_LEFT_BOX_EXTENDED = 0
WIDTH_LOGO = 60
UI_FILE_PATH = "gui/ui/UI.ui"
KEYS_LEFT_BOX_MENU = ['src_webcam']


class SHOWWINDOW(QMainWindow, BASEWINDOW):
    def __init__(self):
        super().__init__()
        self.is_playing = False
        self.current_model = None
        self.current_workpath = os.getcwd()
        self.inputPath = None
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
        self.ui.maximizeButton.clicked.connect(self.maxorRestore)
        self.ui.minimizeButton.clicked.connect(self.showMinimized)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.topbox.doubleClickFrame.connect(self.maxorRestore)
        # --- 最大化 最小化 关闭 --- #

        # --- 播放 暂停 停止 --- #
        self.ui.run_button.setIcon(QIcon(f"{self.current_workpath}/gui/images/newsize/play.png"))
        # --- 播放 暂停 停止 --- #

        # --- 自动加载/动态改变 PT 模型 --- #
        self.pt_Path = f"{self.current_workpath}/cv_module/ptfiles/"
        os.makedirs(self.pt_Path, exist_ok=True)
        self.pt_list = os.listdir(f'{self.current_workpath}/cv_module/ptfiles/')
        self.pt_list = [file for file in self.pt_list if file.endswith('.pt')]
        self.pt_list.sort(key=lambda x: os.path.getsize(f'{self.current_workpath}/cv_module/ptfiles/' + x))
        self.ui.model_box.clear()
        self.ui.model_box.addItems(self.pt_list)
        self.loadModels()
        self.ui.model_box.currentTextChanged.connect(self.changeModel)
        # --- 自动加载/动态改变 PT 模型 --- #

        self.ui.src_cam.clicked.connect(self.selectWebcam)
        self.ui.src_database.clicked.connect(self.showTableResult)

        # --- 状态栏 初始化 --- #
        self.shadowStyle(self.ui.mainBody, QColor(0, 0, 0, 38), top_bottom=['top', 'bottom'])
        self.model_name = self.ui.model_box.currentText()  # 获取默认 model
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

        # --- MessageBar Init --- #
        self.showStatus("Welcome to SGMS")
        # --- MessageBar Init --- #

        # Control Function (TEST)
        self.ui.control_button.setCheckable(True)
        self.ui.control_button.setIcon(QIcon('gui/images/icon.png'))
        self.ui.control_button.clicked.connect(self.start_control)

    def initThreads(self):
        self.yolo_threads = ThreadPool()
        # 获取当前Model
        model_name = self.checkCurrentModel()
        if model_name:
            self.yolo_threads.set(model_name, MODEL_THREAD_CLASSES[model_name]())
            self.initModel(yoloname=model_name)

    # 加载 pt 模型到 model_box
    def loadModels(self):
        pt_list = os.listdir(f'{self.current_workpath}/cv_module/ptfiles/')
        pt_list = [file for file in pt_list if file.endswith('.pt')]
        pt_list.sort(key=lambda x: os.path.getsize(f'{self.current_workpath}/cv_module/ptfiles/' + x))

        if pt_list != self.pt_list:
            self.pt_list = pt_list
            self.ui.model_box.clear()
            self.ui.model_box.addItems(self.pt_list)

    def stopOtherModelProcess(self, model_name, current_yoloname):
        yolo_thread = self.yolo_threads.get(model_name)
        yolo_thread.finished.connect(lambda: self.resignModel(current_yoloname))
        yolo_thread.stop_dtc = True
        self.yolo_threads.stop_thread(model_name)

    # 停止其他模型
    def stopOtherModel(self, current_yoloname=None):
        for model_name in self.yolo_threads.threads_pool.keys():
            if not current_yoloname or model_name == current_yoloname:
                continue
            if self.yolo_threads.get(model_name).isRunning():
                self.stopOtherModelProcess(model_name, current_yoloname)

    # 重新加载模型
    def resignModel(self, model_name):
        # 重载 common 和 yolo 模块
        glo.set_value('yoloname', model_name)
        self.reloadModel()
        self.yolo_threads.set(model_name, MODEL_THREAD_CLASSES[model_name]())
        self.initModel(yoloname=model_name)
        self.runModel(True)

    # Model 变化
    def changeModel(self):
        self.model_name = self.ui.model_box.currentText()
        model_name = self.checkCurrentModel()
        if not model_name:
            return
        # 停止其他模型
        self.stopOtherModel(model_name)
        yolo_thread = self.yolo_threads.get(model_name)
        if yolo_thread is not None:
            yolo_thread.new_model_name = f'{self.current_workpath}/cv_module/ptfiles/' + self.ui.model_box.currentText()
        else:
            self.yolo_threads.set(model_name, MODEL_THREAD_CLASSES[model_name]())
            self.initModel(yoloname=model_name)
            self.loadConfig()
            self.showStatus(f"Change Model to {model_name} Successfully")

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
        current_model_name = self.checkCurrentModel()
        if current_model_name is not None:
            self.runModelProcess(current_model_name)
        else:
            self.showStatus('The current model is not supported')
            if self.ui.run_button.isChecked():
                self.ui.run_button.setChecked(False)

    # 开始/暂停 预测
    def runorContinue(self):
        if self.inputPath is not None:
            self.is_playing = not self.is_playing
            icon_path = "gui/images/newsize/pause.png" if self.is_playing else "gui/images/newsize/play.png"
            self.ui.run_button.setIcon(QIcon())
            self.ui.run_button.setIcon(QIcon(icon_path))
            self.changeModel()
            self.runModel()
        else:
            self.showStatus("Please select the Image/Video before starting detection...")
            self.ui.run_button.setChecked(False)

    # 停止识别
    def stopDetect(self):
        self.controller.terminate()
        self.controller.wait()
        self.is_controling = False
        self.showStatus('Gesture Controller Stopped')
        self.quitRunningModel(stop_status=True)
        self.is_playing = False
        self.ui.run_button.setChecked(False)
        self.ui.run_button.setIcon(QIcon(f"{self.current_workpath}/gui/images/newsize/play.png"))
        self.ui.main_rightbox.clear()
