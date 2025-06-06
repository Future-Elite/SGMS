import json
import os
import threading
from collections import deque
import mediapipe as mp
import cv2
import numpy as np
import pyautogui
import time
import subprocess
import win32com.client
import keyboard
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom

# ================== 全局初始化 ==================
# 初始化音量控制
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_ctl = cast(interface, POINTER(IAudioEndpointVolume))

# 用户自定义软件路径配置
PPT_PATH = r"C:\Users\29740\Desktop\需求分析和可行性分析.pptx"
MUSIC_PATH = r"E:\网易云音乐\CloudMusic\cloudmusic.exe"


# ================== PowerPoint初始化 ==================
def initialize_powerpoint():
    """根据指定路径初始化PPT应用"""
    pythoncom.CoInitialize()  # 确保COM线程安全

    def check_ppt_process():
        try:
            output = subprocess.check_output('tasklist', shell=True).decode('gbk')
            return 'POWERPNT.EXE' in output
        except Exception as e:
            print(f"进程检查失败: {str(e)}")
            return False

    try:
        # 尝试连接已有实例
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        return ppt_app
    except Exception as e:
        print(f"连接PowerPoint失败: {str(e)}，尝试启动新实例...")
        try:
            if not check_ppt_process():
                print("正在启动PowerPoint...")
                subprocess.Popen(PPT_PATH)
                time.sleep(5)  # 等待PPT启动
            return win32com.client.Dispatch("PowerPoint.Application")
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
        self.current_gesture = None
        self.mouse_control_active = False
        self.last_gesture = None
        self.media_control_lock = False
        self.interval_activated = False
        self.interval_timeout = 10
        self.interval_activate_time = None
        self.actions = {
            0: self._action_wrapper(self.left_double_click),
            1: self._action_wrapper(self.backward),
            2: self._action_wrapper(self.forward),
            3: self._action_wrapper(self.high),
            4: self._action_wrapper(self.left_click),
            5: self._action_wrapper(self.low),
            6: self._action_wrapper(self.mouse_control_loop),
            7: self._action_wrapper(self.activate),
            8: self._action_wrapper(self.right_click),
            9: self._action_wrapper(self.start_or_pause)
        }
        self.slide_show_active = False

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
        pyautogui.doubleClick()
        print("左键双击")

    def activate(self):
        self.mouse_control_active = False
        print("激活手势已确认")

    def start_or_pause(self):
        """智能播放/暂停控制"""
        try:
            # 优先处理PPT放映模式
            if self._check_ppt_slideshow():
                print("PPT放映中，发送空格键翻页")
                pyautogui.press('space')
                return

            # 系统级媒体控制
            keyboard.press_and_release('play/pause')
            print("发送全局播放/暂停指令")

            # 异常回退：发送备用空格键
            time.sleep(0.3)
            if not self._check_media_activity():
                pyautogui.press('space')
                print("尝试空格键回退")

        except Exception as e:
            print(f"播放控制异常: {e}")
            pyautogui.hotkey('ctrl', 'alt', 'p')  # 终极回退方案

    def _check_media_activity(self):
        """通过音频会话检测媒体活动状态"""
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                if session.Process and session.Process.name() in ('cloudmusic.exe', 'vlc.exe', 'potplayermini64.exe'):
                    volume = session.SimpleAudioVolume
                    if volume.GetMute() == 0 and volume.GetMasterVolume() > 0:
                        return True
            return False
        except Exception as e:
            print(f"媒体状态检测异常: {e}")
            return False

    def _check_ppt_slideshow(self):
        """检查PPT是否处于放映模式"""
        try:
            if ppt_app and ppt_app.SlideShowWindows.Count > 0:
                self.slide_show_active = True
                return True
            self.slide_show_active = False
            return False
        except Exception as e:
            print(f"PPT状态检查失败: {e}")
            self.slide_show_active = False
            return False

    def backward(self):
        try:
            # 检查PPT放映模式
            if self._check_ppt_slideshow():
                # 确保有有效的放映窗口
                if ppt_app.SlideShowWindows.Count > 0:
                    # 使用PPT对象模型控制
                    ppt_app.SlideShowWindows(1).View.Previous()
                    print("PPT上一页（放映模式）")
                return

            # 系统级媒体控制
            if self._check_music_process():
                keyboard.press_and_release('previous track')
                print("媒体上一曲")
            else:
                # 备用方案：发送方向键（适配PDF阅读器等）
                pyautogui.press('left')
                print("发送方向左键")

        except Exception as e:
            print(f"上一页控制异常: {e}")
            # 终极回退方案
            pyautogui.press('left')

    def forward(self):
        try:
            # 检查PPT放映模式
            if self._check_ppt_slideshow():
                # 确保有有效的放映窗口
                if ppt_app.SlideShowWindows.Count > 0:
                    # 使用PPT对象模型控制
                    ppt_app.SlideShowWindows(1).View.Next()
                    print("PPT下一页（放映模式）")
                return

            # 系统级媒体控制
            if self._check_music_process():
                keyboard.press_and_release('next track')
                print("媒体下一曲")
            else:
                # 备用方案：发送方向键（适配PDF阅读器等）
                pyautogui.press('right')
                print("发送方向右键")

        except Exception as e:
            print(f"下一页控制异常: {e}")
            # 终极回退方案
            pyautogui.press('right')

    def right_click(self):
        pyautogui.rightClick()
        print("模拟右键点击")

    def left_click(self):
        pyautogui.click()
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
        hands = mp_hands.Hands(
            static_image_mode=False,  # 改为False提高实时性能
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.4
        )

        screen_w, screen_h = pyautogui.size()
        cap = cv2.VideoCapture('http://localhost:5000/stream')
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
                print("无法从视频流获取帧，尝试重连...")
                cap.release()
                time.sleep(1)
                cap = cv2.VideoCapture('http://localhost:5000/stream')
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            h, w = frame.shape[:2]

            # 检测到手部
            if results.multi_hand_landmarks:
                # 检测到两只手时退出
                if len(results.multi_hand_landmarks) >= 2:
                    print("检测到两只手，退出鼠标控制模式")
                    self.mouse_control_active = False
                    break

                # 只有一只手时继续控制
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
                    # 可视化标记
                    cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)

        cap.release()
        cv2.destroyAllWindows()
        self.mouse_control_active = False
        print("鼠标控制模式结束")

    def handle_gesture(self, gesture):
        if gesture is not None:
            # 激活手势处理
            if gesture == gesture_labels["activate"]:
                self.interval_activated = True
                self.interval_activate_time = time.time()
                print("间隔手势已激活，10秒内等待下一个操作...")
                return

            # 检查激活状态
            if not self.interval_activated:
                print("请先使用激活手势")
                return

            # 检查激活超时
            if time.time() - self.interval_activate_time > self.interval_timeout:
                print("操作超时，请重新激活")
                self.interval_activated = False
                return

            # 执行手势操作
            self.current_gesture = gesture
            if gesture in self.actions:
                if gesture == gesture_labels['mouse']:
                    threading.Thread(target=self.mouse_control_loop, daemon=True).start()
                else:
                    self.actions[gesture]()

            # 重置激活状态
            self.interval_activated = False
            self.interval_activate_time = None
        else:
            print("未识别到有效手势")


def get_gesture():
    """读取手势识别结果"""
    if not os.path.exists('data/config/res.json'):
        return None
    try:
        with open('data/config/res.json', "r") as f:
            data = json.load(f)
            # 获取置信度最高的手势
            return max(data, key=data.get)
    except Exception as e:
        print(f"手势读取失败: {e}")
        return None


if __name__ == "__main__":
    # 初始化音量
    volume_ctl.SetMute(0, None)

    # PPT初始化处理
    if ppt_app:
        try:
            # 清理可能的幻灯片放映
            if ppt_app.SlideShowWindows.Count > 0:
                ppt_app.SlideShowWindows.Item(1).View.Exit()
                print("已关闭现有PPT放映")
            print("PowerPoint控制已初始化")
        except Exception as e:
            print(f"PPT初始化警告: {str(e)}")
    else:
        print("警告: PowerPoint控制功能不可用")

    # 启动手势控制器
    controller = GestureController()
    print("手势控制器已启动...")

    # 主循环
    while True:
        gesture_name = get_gesture()
        if gesture_name:
            print(f'[手势]: {gesture_name}')
            gesture_value = gesture_labels.get(gesture_name.split(' ')[0])
            controller.handle_gesture(gesture_value)
        time.sleep(0.5)  # 降低CPU使用率
