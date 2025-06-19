class StreamRedirector:
    def __init__(self, callback):
        self.callback = callback

    def write(self, msg):
        msg = msg.strip()
        if msg:  # 避免空行触发
            self.callback(msg)

    def flush(self):
        pass  # 需要定义以兼容标准输出接口
