from collections import deque

from PySide6.QtCore import QObject


class GlobalState(QObject):
    # 单例模式确保全局唯一
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_state()
        return cls._instance

    def _init_state(self):
        self.detection_queue = deque(maxlen=10)  # 缓存最近10次检测结果
        self.latest_result = None

    def update_detection(self, data):
        """供YOLOThread调用的更新方法"""
        self.detection_queue.append(data)
        self.latest_result = data

