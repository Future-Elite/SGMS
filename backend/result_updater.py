import threading
import requests
import time
from queue import Queue, Empty, Full


class ResultUpdater:
    def __init__(self, url, max_queue_size=10, min_interval=3):
        self.url = url
        self.result_queue = Queue(maxsize=max_queue_size)
        self.min_interval = min_interval
        self.last_upload_time = 0
        threading.Thread(target=self._upload_loop, daemon=True).start()

    def submit(self, result):
        try:
            # 如果队列满了，丢弃最旧的，保持最新结果在队尾
            if self.result_queue.full():
                try:
                    self.result_queue.get_nowait()
                except Empty:
                    pass
            self.result_queue.put_nowait(result)
        except Full:
            print("Queue is full. Dropping result.")

    def _upload_loop(self):
        while True:
            try:
                # 阻塞等待一个待上传结果
                result = self.result_queue.get(timeout=1)
            except Empty:
                continue

            # 计算距离上次上传是否超过间隔，不够则等待
            now = time.time()
            interval = now - self.last_upload_time
            if interval < self.min_interval:
                time.sleep(self.min_interval - interval)

            # 上传结果
            if result:
                try:
                    response = requests.post(self.url, json=result, timeout=3)
                    if response.status_code == 200:
                        self.last_upload_time = time.time()
                except Exception as e:
                    pass
                # 标记任务完成，队列get解锁
                self.result_queue.task_done()


def gesture_update(message):
    with open('data/config/msg.txt', 'a') as f:
        f.write(message + '\n')
