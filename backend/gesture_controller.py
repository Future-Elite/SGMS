import datetime
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
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from data.models import DeviceState, DeviceTypeEnum
from result_updater import gesture_update

# ================== 全局初始化 ==================
# 初始化音量控制
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_ctl = cast(interface, POINTER(IAudioEndpointVolume))

PPT_PATH = None


# ================== PowerPoint初始化 ==================
def initialize_powerpoint():
    """根据指定路径初始化PPT应用"""
    pythoncom.CoInitialize()  # 确保COM线程安全

    def check_ppt_process():
        try:
            output = subprocess.check_output('tasklist', shell=True).decode('gbk')
            return 'POWERPNT.EXE' in output
        except Exception as e:
            gesture_update(f"进程检查失败: {str(e)}")
            return False

    try:
        # 尝试连接已有实例
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        return ppt_app
    except Exception as e:
        gesture_update(f"连接PowerPoint失败: {str(e)}，尝试启动新实例...")
        try:
            if not check_ppt_process():
                gesture_update("正在启动PowerPoint...")
                subprocess.Popen(PPT_PATH)
                time.sleep(5)  # 等待PPT启动
            return win32com.client.Dispatch("PowerPoint.Application")
        except Exception as e:
            gesture_update(f"PowerPoint启动失败: {str(e)}")
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

engine = create_engine("sqlite:///data/database.db")
Session = sessionmaker(bind=engine)
session = Session()


def get_gesture():
    """读取手势识别结果"""
    if not os.path.exists('data/config/res.json'):
        return None
    try:
        with open('data/config/res.json', "r") as f:
            data = json.load(f)
            # 获取置信度最高的手势
            return max(data, key=data.get) if data else None
    except Exception as e:
        gesture_update(f"手势读取失败: {e}")
        return None


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
        self.slide_show_active = False
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
                before = self.get_device_state_snapshot()
                func()
                after = self.get_device_state_snapshot()
                self.verify_command_effect(before, after)
                self.save_device_state(after)
                self.last_gesture = self.current_gesture
                self._set_cooldown()

        return wrapped

    def get_device_state_snapshot(self):
        """获取当前设备状态"""
        return {
            'volume': volume_ctl.GetMasterVolumeLevelScalar(),
            'mouse_control_active': self.mouse_control_active,
            'ppt_slide_show_active': self._check_ppt_slideshow()
        }

    def save_device_state(self, state, device_type="tv", device_id="system"):
        record = DeviceState(
            device_type=DeviceTypeEnum[device_type],
            device_id=device_id,
            current_state=state,
            last_updated=datetime.datetime.now()
        )
        session.merge(record)
        session.commit()

    def verify_command_effect(self, before_state, after_state, expected_keys=None):
        """验证命令执行是否生效"""
        if expected_keys is None:
            expected_keys = before_state.keys()
        changes = {k: (before_state[k], after_state[k]) for k in expected_keys if before_state[k] != after_state[k]}

    def _set_cooldown(self):
        self.media_control_lock = True
        time.sleep(0.5)
        self.media_control_lock = False

    def _check_music_process(self):
        try:
            output = subprocess.check_output('tasklist', shell=True).decode('gbk')
            return 'cloudmusic.exe' in output
        except Exception as e:
            gesture_update(f"检查音乐进程失败: {e}")
            return False

    def left_double_click(self):
        pyautogui.doubleClick()
        gesture_update("左键双击")

    def activate(self):
        self.mouse_control_active = False
        gesture_update("激活手势已确认")

    def start_or_pause(self):
        """智能播放/暂停控制"""
        try:
            # 优先处理PPT放映模式
            if self._check_ppt_slideshow():
                gesture_update("PPT放映中，发送空格键翻页")
                pyautogui.press('space')
                return

            # 系统级媒体控制
            keyboard.press_and_release('play/pause')
            gesture_update("发送全局播放/暂停指令")

            # 异常回退：发送备用空格键
            time.sleep(0.3)
            if not self._check_media_activity():
                pyautogui.press('space')
                gesture_update("尝试空格键回退")

        except Exception as e:
            gesture_update(f"播放控制异常: {e}")
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
            gesture_update(f"媒体状态检测异常: {e}")
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
            gesture_update(f"PPT状态检查失败: {e}")
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
                    gesture_update("PPT上一页（放映模式）")
                return

            # 系统级媒体控制
            if self._check_music_process():
                keyboard.press_and_release('previous track')
                gesture_update("媒体上一曲")
            else:
                pyautogui.press('left')
                gesture_update("发送方向左键")

        except Exception as e:
            gesture_update(f"上一页控制异常: {e}")
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
                    gesture_update("PPT下一页（放映模式）")
                return

            # 系统级媒体控制
            if self._check_music_process():
                keyboard.press_and_release('next track')
                gesture_update("媒体下一曲")
            else:
                pyautogui.press('right')
                gesture_update("发送方向右键")

        except Exception as e:
            gesture_update(f"下一页控制异常: {e}")
            pyautogui.press('right')

    def right_click(self):
        pyautogui.rightClick()
        gesture_update("右键点击")

    def left_click(self):
        pyautogui.click()
        gesture_update("左键点击")

    def high(self):
        current_vol = volume_ctl.GetMasterVolumeLevelScalar()
        new_vol = min(round(current_vol + 0.1, 1), 1.0)
        volume_ctl.SetMasterVolumeLevelScalar(new_vol, None)
        gesture_update(f"音量已升至：{new_vol * 100}%")

    def low(self):
        current_vol = volume_ctl.GetMasterVolumeLevelScalar()
        new_vol = max(round(current_vol - 0.1, 1), 0.0)
        volume_ctl.SetMasterVolumeLevelScalar(new_vol, None)
        gesture_update(f"音量已降至：{new_vol * 100}%")

    def mouse_control_loop(self):
        if self.mouse_control_active:
            gesture_update("鼠标控制已在运行中")
            return

        self.mouse_control_active = True
        gesture_update("启动鼠标控制模式...")

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
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
        # 设置距离阈值（单位：米）
        DISTANCE_THRESHOLD = 0.3  # 30厘米内视为有效触发

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

        # 计算手部到摄像头的距离
        def calculate_distance(hand_landmarks, frame_width, frame_height):
            """估算手部到摄像头的距离"""
            # 计算手部关键点的像素距离
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

            # 计算手腕到中指根部的像素距离
            pixel_distance = np.sqrt(
                (wrist.x - middle_mcp.x) ** 2 * frame_width ** 2 +
                (wrist.y - middle_mcp.y) ** 2 * frame_height ** 2
            )

            # 估算实际距离（经验公式，需根据摄像头参数调整）
            REFERENCE_DISTANCE = 0.15  # 标准手掌参考距离（约15cm）
            REFERENCE_PIXELS = 120  # 在1米距离时的手掌像素宽度

            # 估算距离：参考距离 * 参考像素数 / 当前像素数
            estimated_distance = (REFERENCE_DISTANCE * REFERENCE_PIXELS) / max(pixel_distance, 1)
            return estimated_distance

        while cap.isOpened() and self.mouse_control_active:
            success, frame = cap.read()
            if not success:
                gesture_update("无法从视频流获取帧，尝试重连...")
                cap.release()
                time.sleep(1)
                cap = cv2.VideoCapture('http://localhost:5000/stream')
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            h, w = frame.shape[:2]
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            cv2.putText(frame, f"{current_time}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # 检测到手部
            if results.multi_hand_landmarks:
                # 绘制所有检测到的手
                for hand_landmarks in results.multi_hand_landmarks:
                    # 绘制手部关键点
                    for landmark in hand_landmarks.landmark:
                        cx, cy = int(landmark.x * w), int(landmark.y * h)
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

                # 检测到两只手时检查距离
                if len(results.multi_hand_landmarks) >= 2:
                    # 计算第二只手的距离
                    second_hand = results.multi_hand_landmarks[1]
                    distance = calculate_distance(second_hand, w, h)

                    # 在图像上显示距离信息
                    cv2.putText(frame, f"Second Hand Dist: {distance:.2f}m", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    # 检查距离是否在阈值范围内
                    if distance < DISTANCE_THRESHOLD:
                        gesture_update(f"检测到第二只手（距离：{distance:.2f}m），退出鼠标控制模式")
                        self.mouse_control_active = False
                        break
                    else:
                        # 距离过远，继续控制
                        gesture_update(f"检测到第二只手但距离过远（{distance:.2f}m），继续控制")
                        pass

                # 只有一只手时继续控制（选择最前面的手）
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

                    # 显示鼠标位置信息
                    cv2.putText(frame, f"Mouse: ({int(final_x)}, {int(final_y)})",
                                (w - 400, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            # 显示状态信息
            cv2.putText(frame, "Mouse Control: ACTIVE", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f"Mode: {'Mouse' if self.mouse_control_active else 'Inactive'}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # 显示视频流（用于调试）
            # cv2.imshow("Gesture Mouse Control", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.mouse_control_active = False
                break

        cap.release()
        cv2.destroyAllWindows()
        self.mouse_control_active = False
        gesture_update("鼠标控制模式结束")

    def handle_gesture(self, gesture):
        if gesture is not None:
            # 激活手势处理
            if gesture == gesture_labels["activate"]:
                self.interval_activated = True
                self.interval_activate_time = time.time()
                gesture_update("间隔手势已激活，10秒内等待下一个操作...")
                return

            # 检查激活状态
            if not self.interval_activated:
                gesture_update("请先使用激活手势")
                return

            # 检查激活超时
            if time.time() - self.interval_activate_time > self.interval_timeout:
                gesture_update("操作超时，请重新激活")
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
            gesture_update("未识别到有效手势")


if __name__ == "__main__":
    # 初始化音量
    volume_ctl.SetMute(0, None)

    # PPT初始化处理
    if ppt_app:
        try:
            # 清理可能的幻灯片放映
            if ppt_app.SlideShowWindows.Count > 0:
                ppt_app.SlideShowWindows.Item(1).View.Exit()
                gesture_update("已关闭现有PPT放映")
            gesture_update("PowerPoint控制已初始化")
        except Exception as e:
            gesture_update(f"PPT初始化警告: {str(e)}")
    else:
        gesture_update("警告: PowerPoint控制功能不可用")

    # 启动手势控制器
    controller = GestureController()
    gesture_update("手势控制器已启动")

    # 主循环
    while True:
        gesture_name = get_gesture()
        if gesture_name:
            gesture_value = gesture_labels.get(gesture_name.split(' ')[0])
            controller.handle_gesture(gesture_value)
        time.sleep(0.5)