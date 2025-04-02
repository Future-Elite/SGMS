from collections import deque
import threading
import time


class BackendController:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_state()
        return cls._instance

    def _init_state(self):
        self.detection_queue = deque(maxlen=10)
        self.processing_thread = None
        self.running = False
        self.current_action = None

    def start_processing(self):
        if not self.running:
            self.running = True
            self.processing_thread = threading.Thread(target=self._process_queue)
            self.processing_thread.daemon = True
            self.processing_thread.start()

    def stop_processing(self):
        self.running = False
        if self.processing_thread:
            self.processing_thread.join()

    def update(self, data):
        with self._lock:
            self.detection_queue.append(data)

    def _process_queue(self):
        while self.running:
            with self._lock:
                if self.detection_queue:
                    latest_result = self.detection_queue[-1]
                    self._handle_detection(latest_result)
            time.sleep(0.5)

    def _handle_detection(self, detection):
        action = detection.keys() if detection else None
        self.current_action = action

        if action == 'volume_up':
            self._volume_up()
        elif action == 'volume_down':
            self._volume_down()
        elif action == 'mute':
            self._mute()
        elif action is None:
            print("No action detected.")
        else:
            print("Unknown action", action)

    def _volume_up(self):
        print("VOLUME UP")
        # Implement actual volume control here

    def _volume_down(self):
        print("VOLUME DOWN")
        # Implement actual volume control here

    def _mute(self):
        print("MUTE TOGGLED")
        # Implement actual mute control here
