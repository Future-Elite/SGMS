import time
from PySide6.QtCore import QThread, Signal
from frontend.ThreadPool import global_state


class BackendManager(QThread):
    new_data = Signal(dict)  # 定义信号用于传递数据

    def run(self):
        while True:
            data = global_state.latest_result
            if data:
                self.new_data.emit(data)  # 通过信号传递数据
            time.sleep(1)


class BackendThread:
    def __init__(self):
        self.thread = BackendManager()
        self.thread.new_data.connect(self.handle_data)

    def start(self):
        self.thread.start()

    def handle_data(self, data):
        # TODO: 根据智能模块返回的数据进行处理，执行后端服务
        print("Detect:", data)

