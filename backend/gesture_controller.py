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
        self.current_gesture = None
        self.mouse_control_active = False
        self.last_gesture = None
        self.media_control_lock = False
        self.interval_activated = False  # 间隔手势激活状态
        self.interval_timeout = 10  # 间隔手势有效时间延长至2秒
        self.interval_activate_time = None  # 间隔激活时间戳
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

    def start_or_pause(self):
        """智能播放/暂停控制（系统级媒体控制+应用专属控制）"""
        try:
            # 第一优先级：系统级媒体控制（支持大部分播放器）
            keyboard.press_and_release('play/pause')
            print("发送全局播放/暂停指令")

            # 第二优先级：检查特定应用状态
            def check_specific_apps():
                # PowerPoint放映控制
                if ppt_app and ppt_app.SlideShowWindows.Count > 0:
                    print("检测到PPT放映中，禁用媒体控制")
                    return True

                # 网易云音乐进程检测
                if self._check_music_process():
                    print("网易云音乐进程活跃")
                    return False

                return False


            # 异常回退：发送备用空格键（适配网页播放器等）
            time.sleep(0.3)
            if not self._check_media_activity():
                pyautogui.press('space')
                print("尝试空格键回退")

        except Exception as e:
            print(f"播放控制异常: {e}")
            # 终极回退方案
            pyautogui.hotkey('ctrl', 'alt', 'p')  # 预留系统级热键映射

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

    def backward(self):
        try:
            # PowerPoint控制（放映模式优先）
            if ppt_app and ppt_app.SlideShowWindows.Count > 0:
                ppt_app.SlideShowWindows(1).View.Previous()
                print("PPT上一页（放映模式）")
            elif ppt_app and ppt_app.ActivePresentation:
                current_slide = ppt_app.ActivePresentation.SlideShowWindow.View.CurrentShowPosition
                if current_slide > 1:
                    ppt_app.ActivePresentation.SlideShowWindow.View.GotoSlide(current_slide - 1)
                    print("PPT上一页（编辑模式）")
        except Exception as e:
            print(f"PPT控制异常: {e}")
            # 系统级媒体控制
            if self._check_music_process():
                keyboard.press_and_release('previous track')
                print("媒体上一曲")
            else:
                print("无活跃媒体进程")

    def forward(self):
        try:
            # PowerPoint控制
            if ppt_app and ppt_app.SlideShowWindows.Count > 0:
                ppt_app.SlideShowWindows(1).View.Next()
                print("PPT下一页（放映模式）")
            elif ppt_app and ppt_app.ActivePresentation:
                current_slide = ppt_app.ActivePresentation.SlideShowWindow.View.CurrentShowPosition
                total_slides = ppt_app.ActivePresentation.Slides.Count
                if current_slide < total_slides:
                    ppt_app.ActivePresentation.SlideShowWindow.View.GotoSlide(current_slide + 1)
                    print("PPT下一页（编辑模式）")
        except Exception as e:
            print(f"PPT控制异常: {e}")
            # 系统级媒体控制
            if self._check_music_process():
                keyboard.press_and_release('next track')
                print("媒体下一曲")
            else:
                # 备用方案：发送方向键（适配PDF阅读器等）
                pyautogui.press('right')
                print("发送方向右键")

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

    # 修改后的mouse_control_loop方法
    def mouse_control_loop(self):
        if self.mouse_control_active:
            print("鼠标控制已在运行中")
            return

        self.mouse_control_active = True
        print("启动鼠标控制模式...")

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=True,
                               max_num_hands=2,  # 修改：最多检测2只手
                               model_complexity=1,
                               min_detection_confidence=0.5,
                               min_tracking_confidence=0.4)

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
                # 修改点：检测到两只手时退出
                if len(results.multi_hand_landmarks) >= 2:
                    print("检测到两只手，退出鼠标控制模式")
                    self.mouse_control_active = False
                    break  # 立即退出循环

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
                    # 可视化标记（可选）
                    cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)

        cap.release()
        cv2.destroyAllWindows()
        self.mouse_control_active = False
        print("鼠标控制模式结束")

    def handle_gesture(self, gesture):
        if gesture is not None:
            if gesture == gesture_labels["activate"]:
                self.interval_activated = True
                self.interval_activate_time = time.time()
                print("间隔手势已激活，10秒内等待下一个操作...")
            elif self.interval_activated:
                # 检查间隔激活是否超时
                if time.time() - self.interval_activate_time > self.interval_timeout:
                    print("操作超时，间隔手势已重置")
                    self.interval_activated = False
                    self.interval_activate_time = None
                    return

                self.current_gesture = gesture
                if gesture in self.actions:
                    if gesture == gesture_labels['mouse']:
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
        print()


    def start_listening(self):
        while True:
            current_gesture = get_gesture()
            print('[gesture]:', list(current_gesture)[0].split(' ')[0] if current_gesture else None)
            gesture = gesture_labels[list(current_gesture)[0].split(' ')[0]] if current_gesture else None
            self.handle_gesture(gesture)
            time.sleep(1)


def get_gesture():
    if not os.path.exists('data/config/res.json'):
        return None
    try:
        with open('data/config/res.json', "r") as f:
            return json.load(f)
    except Exception as e:
        print("读取失败:", e)
        return None


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
