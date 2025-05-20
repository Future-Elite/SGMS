import importlib
import json
import os
import random
import re
import shutil
import subprocess
import sys

import cv2
import numpy as np

from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QFileDialog, QGraphicsDropShadowEffect
from cv_module.models import common, experimental, yolo
from cv_module.CVThread import YOLOThread
from frontend.ResultWindow import ResultWindow
from gui.ui.utils.webCamera import Camera
from frontend.utils import glo
from frontend.utils.logger import LoggerUtils

glo.init()
glo.set_value('yoloname', "yolov8 yolov11")

GLOBAL_WINDOW_STATE = True
WIDTH_LEFT_BOX_STANDARD = 240
WIDTH_LEFT_BOX_EXTENDED = 240
WIDTH_SETTING_BAR = 290
WIDTH_LOGO = 60
KEYS_LEFT_BOX_MENU = ['src_webcam', 'src_folder', 'src_camera']

# 模型名称和线程类映射
MODEL_THREAD_CLASSES = {
    "yolov8": YOLOThread,
    "yolov11": YOLOThread,
}

# 扩展MODEL_THREAD_CLASSES字典
MODEL_NAME_DICT = list(MODEL_THREAD_CLASSES.items())
for key, value in MODEL_NAME_DICT:
    MODEL_THREAD_CLASSES[f"{key}_left"] = value
    MODEL_THREAD_CLASSES[f"{key}_right"] = value

loggertool = LoggerUtils()


class BASEWINDOW:
    def __init__(self):
        super().__init__()

        self.is_controling = None
        self.controller = None
        self.current_workpath = None
        self.ui = None
        self.result_window = None
        self.inputPath = None
        self.yolo_threads = None
        self.result_statistic = None
        self.detect_result = None
        self.allModelNames = ["yolov8", "yolov11"]

    # 初始化左侧菜单栏
    def initSiderWidget(self):
        # --- 侧边栏 --- #
        self.ui.leftBox.setFixedWidth(WIDTH_LEFT_BOX_STANDARD)

        # 显示用户信息
        self.ui.user_info.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
                                        "color: rgba(0, 0, 0, 140);")
        self.ui.user_info.setReadOnly(True)
        self.ui.user_info.append('User:{0}\nResponse:{1}'.format(glo.get_value('user_name'),
                                                                 glo.get_value('resp'),
                                                                 ))

    # 加载模型
    def initModel(self, yoloname=None):
        thread = self.yolo_threads.get(yoloname)
        if not thread:
            raise ValueError(f"No thread found for '{yoloname}'")
        thread.new_model_name = f'{self.current_workpath}/ptfiles/' + self.ui.model_box.currentText()
        thread.progress_value = self.ui.progress_bar.maximum()
        thread.send_output.connect(lambda x: self.showImg(x, self.ui.main_rightbox, 'img'))
        thread.send_msg.connect(lambda x: self.showStatus(x))
        thread.send_progress.connect(lambda x: self.ui.progress_bar.setValue(x))
        thread.send_fps.connect(lambda x: self.ui.fps_label.setText(str(x)))

    # 阴影效果
    def shadowStyle(self, widget, Color, top_bottom=None):
        shadow = QGraphicsDropShadowEffect()
        if 'top' in top_bottom and 'bottom' not in top_bottom:
            shadow.setOffset(0, -5)
        elif 'bottom' in top_bottom and 'top' not in top_bottom:
            shadow.setOffset(0, 5)
        else:
            shadow.setOffset(5, 5)
        shadow.setBlurRadius(10)  # 阴影半径
        shadow.setColor(Color)  # 阴影颜色
        widget.setGraphicsEffect(shadow)

    # 最大化最小化窗口
    def maxorRestore(self):
        global GLOBAL_WINDOW_STATE
        status = GLOBAL_WINDOW_STATE
        if status:
            # 获取当前屏幕的宽度和高度
            self.showMaximized()
            self.ui.maximizeButton.setStyleSheet("""
                          QPushButton:hover{
                               background-color:rgb(139, 29, 31);
                               border-image: url(:/leftbox/images/newsize/scalling.png);
                           }
                      """)
            GLOBAL_WINDOW_STATE = False
        else:
            self.showNormal()
            self.ui.maximizeButton.setStyleSheet("""
                                      QPushButton:hover{
                                           background-color:rgb(139, 29, 31);
                                           border-image: url(:/leftbox/images/newsize/max.png);
                                       }
                                  """)
            GLOBAL_WINDOW_STATE = True

    # 选择照片/视频 并展示
    def selectFile(self):
        # 获取上次选择文件的路径
        config_file = f'{self.current_workpath}/data/config/file.json'
        config = json.load(open(config_file, 'r', encoding='utf-8'))
        file_path = config['file_path']
        if not os.path.exists(file_path):
            file_path = os.getcwd()
        file, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "Select your Image / Video",  # 标题
            file_path,  # 默认打开路径为当前路径
            "Image / Video type (*.jpg *.jpeg *.png *.bmp *.dib *.jpe *.jp2 *.mp4)"  # 选择类型过滤项，过滤内容在括号中
        )
        if file:
            self.inputPath = file
            glo.set_value('inputPath', self.inputPath)
            # 如果是视频， 显示第一帧
            if ".avi" in self.inputPath or ".mp4" in self.inputPath:
                # 显示第一帧
                self.cap = cv2.VideoCapture(self.inputPath)
                ret, frame = self.cap.read()
                if ret:
                    self.showImg(frame, self.ui.main_leftbox, 'img')
            # 如果是图片 正常显示
            else:
                self.showImg(self.inputPath, self.ui.main_rightbox, 'path')
            self.showStatus('Loaded File：{}'.format(os.path.basename(self.inputPath)))
            config['file_path'] = os.path.dirname(self.inputPath)
            config_json = json.dumps(config, ensure_ascii=False, indent=2)
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_json)

    # 选择摄像头
    def selectWebcam(self):
        try:
            cam_num, cams = Camera().get_cam_num()
            if cam_num > 0:
                cam = cams[0]
                self.showStatus(f'Loaded camera：Camera_{cam}')
                self.inputPath = int(cam)
            else:
                self.showStatus('No camera found')
        except Exception as e:
            self.showStatus('%s' % e)

    # 选择文件夹
    def selectFolder(self):
        config_file = f'{self.current_workpath}/data/config/folder.json'
        config = json.load(open(config_file, 'r', encoding='utf-8'))
        folder_path = config['folder_path']
        if not os.path.exists(folder_path):
            folder_path = os.getcwd()
        FolderPath = QFileDialog.getExistingDirectory(
            self,
            "Select your Folder",
            folder_path  # 起始目录
        )
        if FolderPath:
            FileFormat = [".mp4", ".mkv", ".avi", ".flv", ".jpg", ".png", ".jpeg", ".bmp", ".dib", ".jpe", ".jp2"]
            Foldername = [(FolderPath + "/" + filename) for filename in os.listdir(FolderPath) for jpgname in FileFormat
                          if jpgname in filename]
            self.inputPath = Foldername
            self.showStatus('Loaded Folder：{}'.format(os.path.basename(FolderPath)))
            config['folder_path'] = FolderPath
            config_json = json.dumps(config, ensure_ascii=False, indent=2)
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_json)

    # 显示Label图片
    def showImg(self, img, label, flag):
        try:
            if flag == "path":
                img_src = cv2.imdecode(np.fromfile(img, dtype=np.uint8), -1)
            else:
                img_src = img
            ih, iw, _ = img_src.shape
            w = label.geometry().width()
            h = label.geometry().height()
            # keep original aspect ratio
            if iw / w > ih / h:
                scal = w / iw
                nw = w
                nh = int(scal * ih)
                img_src_ = cv2.resize(img_src, (nw, nh))
            else:
                scal = h / ih
                nw = int(scal * iw)
                nh = h
                img_src_ = cv2.resize(img_src, (nw, nh))

            frame = cv2.cvtColor(img_src_, cv2.COLOR_BGR2RGB)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[2] * frame.shape[1],
                         QImage.Format_RGB888)
            label.setPixmap(QPixmap.fromImage(img))
        except Exception as e:
            print(repr(e))

    # resize 窗口大小
    def resizeGrip(self):
        self.left_grip.setGeometry(0, 10, 10, self.height())
        self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
        self.top_grip.setGeometry(0, 0, self.width(), 10)
        self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    # 导入模块
    def importModel(self):
        # 获取上次选择文件的路径
        config_file = f'{self.current_workpath}/data/config/model.json'
        config = json.load(open(config_file, 'r', encoding='utf-8'))
        self.model_path = config['model_path']
        if not os.path.exists(self.model_path):
            self.model_path = os.getcwd()
        file, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "Select your YOLO Model",  # 标题
            self.model_path,  # 默认打开路径为当前路径
            "Model File (*.pt)"  # 选择类型过滤项，过滤内容在括号中
        )
        if file:
            fileptPath = os.path.join(self.pt_Path, os.path.basename(file))
            if not os.path.exists(fileptPath):
                shutil.copy(file, self.pt_Path)
                self.showStatus('Loaded Model：{}'.format(os.path.basename(file)))
                config['model_path'] = os.path.dirname(file)
                config_json = json.dumps(config, ensure_ascii=False, indent=2)
                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write(config_json)
            else:
                self.showStatus('Model already exists')

    # 查看当前模型
    def checkCurrentModel(self, mode=None):
        # 定义模型和对应条件的映射
        model_conditions = {
            "yolov8": lambda name: "yolov8" in name and not any(
                func(name) for func in [self.checkSegName, self.checkPoseName, self.checkObbName]),
            "yolov11": lambda name: any(sub in name for sub in ["yolov11", "yolo11"]) and not any(
                func(name) for func in [self.checkSegName, self.checkPoseName, self.checkObbName]),
        }

        if mode:
            # VS mode
            model_name = self.model_name1 if mode == "left" else self.model_name2
            model_name = model_name.lower()
            for yoloname, condition in model_conditions.items():
                if condition(model_name):
                    return f"{yoloname}_{mode}"
        else:
            # Single mode
            model_name = self.model_name.lower()
            for yoloname, condition in model_conditions.items():
                if condition(model_name):
                    return yoloname
        return None

    def checkTaskName(self, modelname, taskname):

        if "yolov8" in modelname:
            return bool(re.match(f'yolo.?8.?-{taskname}.*\.pt$', modelname))

        elif "yolo11" in modelname:
            return bool(re.match(f'yolo.?11.?-{taskname}.*\.pt$', modelname))

    # 解决 Modelname 当中的 seg命名问题
    def checkSegName(self, modelname):
        return self.checkTaskName(modelname, "seg")

    # 解决  Modelname 当中的 pose命名问题
    def checkPoseName(self, modelname):
        return self.checkTaskName(modelname, "pose")

    # 解决  Modelname 当中的 pose命名问题
    def checkObbName(self, modelname):
        return self.checkTaskName(modelname, "obb")

    # 停止运行中的模型
    def quitRunningModel(self, stop_status=False):
        for yolo_name in self.yolo_threads.threads_pool.keys():
            try:
                if stop_status:
                    self.yolo_threads.get(yolo_name).stop_dtc = True
                self.yolo_threads.stop_thread(yolo_name)
            except Exception as err:
                loggertool.info(f"Error: {err}")

    # 在MessageBar显示消息
    def showStatus(self, msg):
        self.ui.message_bar.setText(msg)
        if msg == 'Finish Detection':
            self.quitRunningModel()
            self.ui.run_button.setChecked(False)
            self.ui.progress_bar.setValue(0)
        elif msg == 'Stop Detection':
            self.quitRunningModel()
            self.ui.run_button.setChecked(False)
            self.ui.progress_bar.setValue(0)
            self.ui.main_rightbox.clear()
            self.ui.fps_label.setText('--')

    # 导出检测结果 --- 过程代码
    def saveResultProcess(self, outdir, current_model_name, folder):
        yolo_thread = self.yolo_threads.get(current_model_name)
        if folder:
            try:
                output_dir = os.path.dirname(yolo_thread.res_path)
                if not os.path.exists(output_dir):
                    self.showStatus('Please wait for the result to be generated')
                    return
                for filename in os.listdir(output_dir):
                    source_path = os.path.join(output_dir, filename)
                    destination_path = os.path.join(outdir, filename)
                    if os.path.isfile(source_path):
                        shutil.copy(source_path, destination_path)
                self.showStatus('Saved Successfully in {}'.format(outdir))
            except Exception as err:
                self.showStatus(f"Error occurred while saving the result: {err}")
        else:
            try:
                if not os.path.exists(yolo_thread.res_path):
                    self.showStatus('Please wait for the result to be generated')
                    return
                shutil.copy(yolo_thread.res_path, outdir)
                self.showStatus('Saved Successfully in {}'.format(outdir))
            except Exception as err:
                self.showStatus(f"Error occurred while saving the result: {err}")

    def loadAndSetParams(self, config_file, params):
        if not os.path.exists(config_file):
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(params, f, ensure_ascii=False, indent=2)
        else:
            with open(config_file, 'r', encoding='utf-8') as f:
                params.update(json.load(f))
        return params

    # 加载 Setting 栏
    def loadConfig(self):
        # 1、随机初始化超参数，防止切换模型时，超参数不变
        params = {"iou": round(random.uniform(0, 1), 2),
                  "conf": round(random.uniform(0, 1), 2),
                  "delay": random.randint(10, 50),
                  "line_thickness": random.randint(1, 5)}
        self.updateParams(params)
        # 2、绑定配置项超参数
        params = {"iou": 0.45, "conf": 0.25, "delay": 10, "line_thickness": 3}
        params = self.loadAndSetParams('data/config/setting.json', params)
        self.updateParams(params)

    # 更新Config超参数
    def updateParams(self, params):
        self.ui.iou_spinbox.setValue(params['iou'])
        self.ui.iou_slider.setValue(int(params['iou'] * 100))
        self.ui.conf_spinbox.setValue(params['conf'])
        self.ui.conf_slider.setValue(int(params['conf'] * 100))
        self.ui.speed_spinbox.setValue(params['delay'])
        self.ui.speed_slider.setValue(params['delay'])
        self.ui.line_spinbox.setValue(params['line_thickness'])
        self.ui.line_slider.setValue(params['line_thickness'])

    # 重载模型
    def reloadModel(self):
        importlib.reload(common)
        importlib.reload(yolo)
        importlib.reload(experimental)

    def use_mp(self, use_mp):
        for yolo_thread in self.yolo_threads.threads_pool.values():
            yolo_thread.use_mp = use_mp

    def start_control(self):
        if not self.is_controling:
            self.controller = subprocess.Popen(
                [sys.executable, 'backend/gesture_controller.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.is_controling = True
            self.showStatus('Gesture Controller Started')

        else:
            self.controller.terminate()
            self.controller.wait()
            self.is_controling = False
            self.showStatus('Gesture Controller Stopped')

    # 调整超参数
    def changeValue(self, x, flag):
        if flag == 'iou_spinbox':
            self.ui.iou_slider.setValue(int(x * 100))  # The box value changes, changing the slider
        elif flag == 'iou_slider':
            self.ui.iou_spinbox.setValue(x / 100)  # The slider value changes, changing the box
            self.showStatus('IOU Threshold: %s' % str(x / 100))
            for yolo_thread in self.yolo_threads.threads_pool.values():
                yolo_thread.iou_thres = x / 100
        elif flag == 'conf_spinbox':
            self.ui.conf_slider.setValue(int(x * 100))
        elif flag == 'conf_slider':
            self.ui.conf_spinbox.setValue(x / 100)
            self.showStatus('Conf Threshold: %s' % str(x / 100))
            for yolo_thread in self.yolo_threads.threads_pool.values():
                yolo_thread.conf_thres = x / 100
        elif flag == 'speed_spinbox':
            self.ui.speed_slider.setValue(x)
        elif flag == 'speed_slider':
            self.ui.speed_spinbox.setValue(x)
            self.showStatus('Delay: %s ms' % str(x))
            for yolo_thread in self.yolo_threads.threads_pool.values():
                yolo_thread.speed_thres = x  # ms
        elif flag == 'line_spinbox':
            self.ui.line_slider.setValue(x)
        elif flag == 'line_slider':
            self.ui.line_spinbox.setValue(x)
            self.showStatus('Line Width: %s' % str(x))
            for yolo_thread in self.yolo_threads.threads_pool.values():
                yolo_thread.line_thickness = x

    # 展示表格结果
    def showTableResult(self):
        self.result_window = ResultWindow()
        self.result_window.show()
