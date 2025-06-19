import json
import os
import random
import subprocess
import sys

import cv2
import numpy as np

from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from data.models import User
from cv_module.CVThread import CVThread
from frontend.FloatingWindow import FloatingWindow
from frontend.ResultWindow import ResultWindow
from frontend.utils import glo, pipe
from frontend.utils.logger import LoggerUtils
from PySide6.QtWidgets import QMainWindow

glo.init()
glo.set_value('yoloname', "yolov11")

USER = None
# 模型名称和线程类映射
MODEL_THREAD_CLASSES = {
    "yolov11": CVThread,
}

# 扩展MODEL_THREAD_CLASSES字典
MODEL_NAME_DICT = list(MODEL_THREAD_CLASSES.items())
for key, value in MODEL_NAME_DICT:
    MODEL_THREAD_CLASSES[f"{key}_left"] = value
    MODEL_THREAD_CLASSES[f"{key}_right"] = value

loggertool = LoggerUtils()


def get_send_out():
    with pipe.frame_lock:
        if pipe.frame is not None:
            return pipe.frame.copy()
        else:
            return cv2.imread("gui/ui/icon.png")


class BASEWINDOW(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model_name = 'cv_module/ptfiles/yolo11s-cls.pt'
        self.floating_window = None
        self.is_controling = None
        self.controller = None
        self.current_workpath = None
        self.ui = None
        self.result_window = None
        self.yolo_threads = None
        self.result_statistic = None
        self.detect_result = None
        self.allModelNames = ["yolov11"]

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

    # 初始化左侧菜单栏
    def initSiderWidget(self):
        global USER
        # 显示用户信息
        self.ui.user_info.setStyleSheet(u"""
            font: 10pt "Cascadia Mono";
            color: #CCCCCC;  
            background-color: #0C0C0C; 
            border: 1px solid rgb(100, 100, 100);
            border-radius: 4px; 
        """)
        USER = glo.get_value('user')

    # 加载模型
    def initModel(self, yoloname=None):
        thread = self.yolo_threads.get(yoloname)
        thread.model_name = f'{self.current_workpath}/cv_module/ptfiles/yolo11s-cls.pt'
        thread.send_output.connect(lambda x: self.showImg(x, self.ui.main_rightbox, 'img'))
        thread.send_msg.connect(lambda x: self.showStatus(x))

    def float_window(self):
        if self.is_controling:
            self.floating_window = FloatingWindow(get_send_out)
            self.floating_window.show()
            self.showMinimized()

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
        msg = '{0} >> {1}'.format(USER, msg)
        last_msg = self.ui.user_info.toPlainText().split('\n')[-1]
        if msg != last_msg:
            self.ui.user_info.append(msg)
        if 'Finish Detection' in msg:
            self.quitRunningModel()
            self.ui.run_button.setChecked(False)
        elif 'Stop Detection' in msg:
            self.quitRunningModel()
            self.ui.run_button.setChecked(False)
            self.ui.main_rightbox.clear()

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
                  "conf": round(random.uniform(0, 1), 2)}
        self.updateParams(params)
        # 2、绑定配置项超参数
        params = {"iou": 0.45, "conf": 0.25}
        params = self.loadAndSetParams('data/config/setting.json', params)
        self.updateParams(params)

    # 更新Config超参数
    def updateParams(self, params):
        self.ui.iou_spinbox.setValue(params['iou'])
        self.ui.iou_slider.setValue(int(params['iou'] * 100))
        self.ui.conf_spinbox.setValue(params['conf'])
        self.ui.conf_slider.setValue(int(params['conf'] * 100))

    def start_control(self):
        self.controller = subprocess.Popen(
            [sys.executable, 'backend/gesture_controller.py'],
            stdout=sys.stdout, stderr=sys.stdout
        )
        self.is_controling = True
        self.showStatus('Gesture Controller Started')

    def stop_control(self):
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
            for yolo_thread in self.yolo_threads.threads_pool.values():
                yolo_thread.iou_thres = x / 100
        elif flag == 'conf_spinbox':
            self.ui.conf_slider.setValue(int(x * 100))
        elif flag == 'conf_slider':
            self.ui.conf_spinbox.setValue(x / 100)
            for yolo_thread in self.yolo_threads.threads_pool.values():
                yolo_thread.conf_thres = x / 100


    def showTableResult(self):
        global USER
        engine = create_engine('sqlite:///data/database.db', echo=False)
        session = scoped_session(sessionmaker(bind=engine))
        u = None
        if 'Admin' in USER:
            u = USER[7:]
        elif 'User' in USER:
            u = USER[6:]
        user = session.query(User).filter_by(username=u).first()
        session.close()
        if user and not user.is_admin:
            # 不是管理员，只允许查看 OperationLog
            self.result_window = ResultWindow(allowed_tables=["device_state", "operation_log"], current_user=user)
        else:
            # 是管理员，允许查看所有内容
            self.result_window = ResultWindow()
        self.result_window.show()
