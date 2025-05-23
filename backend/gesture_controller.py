import threading
from collections import deque
import mediapipe as mp
import cv2
import numpy as np
import pyautogui
import requests
import time
import subprocess
import win32com.client
import keyboard
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ================== 全局初始化 ==================
# 初始化音量控制
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_ctl = cast(interface, POINTER(IAudioEndpointVolume))

# 用户自定义软件路径配置
PPT_PATH = r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"
MUSIC_PATH = r"E:\网易云音乐\CloudMusic\cloudmusic.exe"


# ================== PowerPoint初始化 ==================
def initialize_powerpoint():
    """根据指定路径初始化PPT应用"""

    def check_ppt_process():
        try:
            output = subprocess.check_output('tasklist', shell=True).decode('gbk')
            return 'POWERPNT.EXE' in output
        except Exception as e:
            print(f"进程检查失败: {str(e)}")
            return False

    try:
        # 尝试连接已有实例
        ppt_app = win32com.client.gencache.EnsureDispatch("PowerPoint.Application")
        return ppt_app
    except:
        # 启动新实例
        try:
            if not check_ppt_process():
                print("正在启动PowerPoint...")
                subprocess.Popen(PPT_PATH)
                time.sleep(5)
            return win32com.client.gencache.EnsureDispatch("PowerPoint.Application")
        except Exception as e:
            print(f"PowerPoint启动失败: {str(e)}")
            return None


ppt_app = initialize_powerpoint()

# ================== 手势标签映射 ==================
gesture_labels = {
        'Left_Double_Click': 0,
        'backward': 1,
        'forward': 2,
        'high': 3,
        'left_click': 4,
        'low': 5,
        'mouse': 6,
        'activate': 7,
        'right_click': 8,
        'start_or_pause': 9
    }


# ================== 手势控制器类 ==================
class GestureController:
    def __init__(self):
        self.mouse_control_active = False
        self.last_gesture = None
        self.media_control_lock = False
        self.interval_activated = False  # 间隔手势激活状态
        self.interval_timeout = 2  # 间隔手势有效时间延长至2秒
        self.interval_activate_time = None  # 间隔激活时间戳
        self.actions = {
            0: self._action_wrapper(self.left_double_click),
            1: self._action_wrapper(self.backward),
            2: self._action_wrapper(self.forward),
            3: self._action_wrapper(self.high),
            4: self._action_wrapper(self.left_click),
            5: self._action_wrapper(self.low),
            6: self._action_wrapper(self.mouse_control_loop),
            # 7: self._action_wrapper(self.activate),
            8: self._action_wrapper(self.right_click),
            9: self._action_wrapper(self.start_or_pause)
        }

    def _action_wrapper(self, func):
        def wrapped():
            if not self.media_control_lock:
                func()
                self.last_gesture = self.current_gesture
                self._set_cooldown()

        return wrapped

    def _set_cooldown(self):
        self.media_control_lock = True
        time.sleep(0.5)
        self.media_control_lock = False

    def _check_music_process(self):
        try:
            output = subprocess.check_output('tasklist', shell=True).decode('gbk')
            return 'cloudmusic.exe' in output
        except Exception as e:
            print(f"检查音乐进程失败: {e}")
            return False

    def left_double_click(self):
        pass

    # def activate(self):
    #     pass

    def start_or_pause(self):
        pass

    def backward(self):
        pass

    def forward(self):
        pass

    def right_click(self):
        keyboard.press_and_release('right')
        print("模拟右键点击")

    def left_click(self):
        keyboard.press_and_release('left')
        print("左键点击")

    def high(self):
        current_vol = volume_ctl.GetMasterVolumeLevelScalar()
        new_vol = min(round(current_vol + 0.1, 1), 1.0)
        volume_ctl.SetMasterVolumeLevelScalar(new_vol, None)
        print(f"音量已升至：{new_vol * 100}%")

    def low(self):
        current_vol = volume_ctl.GetMasterVolumeLevelScalar()
        new_vol = max(round(current_vol - 0.1, 1), 0.0)
        volume_ctl.SetMasterVolumeLevelScalar(new_vol, None)
        print(f"音量已降至：{new_vol * 100}%")

    def mouse_control_loop(self):
        if self.mouse_control_active:
            print("鼠标控制已在运行中")
            return

        self.mouse_control_active = True
        print("启动鼠标控制模式...")

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=True,
                               max_num_hands=1,
                               model_complexity=1,
                               min_detection_confidence=0.5,
                               min_tracking_confidence=0.4)

        screen_w, screen_h = pyautogui.size()
        cap = cv2.VideoCapture(0)
        frame_margin = 30
        smooth_window = 3
        velocity_queue = deque(maxlen=5)
        coord_history = deque(maxlen=smooth_window)

        def adaptive_smooth(new_x, new_y):
            if coord_history:
                prev_x, prev_y = coord_history[-1]
                velocity = np.hypot(new_x - prev_x, new_y - prev_y)
                velocity_queue.append(velocity)
            else:
                velocity = 0
            avg_velocity = np.mean(velocity_queue) if velocity_queue else 0
            alpha = max(0.3, 1 - avg_velocity / 200)
            if coord_history:
                last_x, last_y = coord_history[-1]
                smoothed_x = new_x * (1 - alpha) + last_x * alpha
                smoothed_y = new_y * (1 - alpha) + last_y * alpha
            else:
                smoothed_x, smoothed_y = new_x, new_y
            coord_history.append((smoothed_x, smoothed_y))
            return np.mean([x for x, y in coord_history]), np.mean([y for x, y in coord_history])

        while cap.isOpened() and self.mouse_control_active:
            success, frame = cap.read()
            if not success:
                continue
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            h, w = frame.shape[:2]
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                cx = int(index_tip.x * w)
                cy = int(index_tip.y * h)
                if frame_margin < cx < w - frame_margin and frame_margin < cy < h - frame_margin:
                    x_ratio = (cx - frame_margin) / (w - 2 * frame_margin)
                    y_ratio = (cy - frame_margin) / (h - 2 * frame_margin)
                    mapped_x = screen_w * (x_ratio ** 1.3)
                    mapped_y = screen_h * (y_ratio ** 1.3)
                    final_x, final_y = adaptive_smooth(mapped_x, mapped_y)
                    pyautogui.moveTo(int(screen_w - final_x), int(final_y), duration=0.001, _pause=False)
                    cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
            cv2.imshow('Precision Tracker', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.mouse_control_active = False
        print("鼠标控制模式结束")

    def handle_gesture(self, gesture):
        if gesture is not None:


            if gesture == gesture_labels["activate"]:
                self.interval_activated = True
                self.interval_activate_time = time.time()
                print("间隔手势已激活，2秒内等待下一个操作...")
            elif self.interval_activated:
                # 检查间隔激活是否超时
                if time.time() - self.interval_activate_time > self.interval_timeout:
                    print("操作超时，间隔手势已重置")
                    self.interval_activated = False
                    self.interval_activate_time = None
                    return

                self.current_gesture = gesture
                if gesture in self.actions:
                    if gesture == 'mouse':
                        threading.Thread(target=self.mouse_control_loop).start()
                    else:
                        self.actions[gesture]()
                    self.interval_activated = False
                    self.interval_activate_time = None
            else:
                print("无效手势")
                self.last_gesture = None
        else:
            print("请先使用间隔手势激活操作")



    def start_listening(self):
        while True:
            current_gesture = get_gesture_from_flask()
            self.handle_gesture(current_gesture)
            time.sleep(0.2)


# ================== Flask通信模块 ==================
def get_gesture_from_flask():
    try:
        response = requests.get('http://localhost:5000/result')
        print(response.json())
        if response.status_code == 200:
            return gesture_labels.get(response.json(), None)
        return None
    except Exception as e:
        print(f"请求异常：{e}")
        return None


# ================== 主程序入口 ==================
if __name__ == "__main__":
    volume_ctl.SetMute(0, None)

    if ppt_app:
        try:
            # 清理可能的幻灯片放映
            if ppt_app.SlideShowWindows.Count > 0:
                ppt_app.SlideShowWindows.Item(1).View.Exit()
            print("PowerPoint控制已初始化")
        except Exception as e:
            print(f"初始化警告：{str(e)}")
    else:
        print("警告: PowerPoint控制功能不可用")

    controller = GestureController()
    print("手势控制器已启动（支持常规PPT编辑模式）...")
    controller.start_listening()
