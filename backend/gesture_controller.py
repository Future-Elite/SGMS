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
    "start": 0,
    "pause": 1,
    "forward": 2,
    "backward": 3,
    "high": 4,
    "low": 5
}


# ================== 手势控制器类 ==================
class GestureController:
    def __init__(self):
        self.last_gesture = None
        self.media_control_lock = False
        self.interval_activated = False  # 间隔手势激活状态
        self.interval_timeout = 2  # 间隔手势有效时间延长至2秒
        self.interval_activate_time = None  # 间隔激活时间戳
        self.actions = {
            0: self._action_wrapper(self.play_music),
            2: self._action_wrapper(self.handle_forward),
            3: self._action_wrapper(self.handle_backward),
            4: self._action_wrapper(self.volume_up),
            5: self._action_wrapper(self.volume_down)
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

    def play_music(self):
        try:
            if not self._check_music_process():
                subprocess.Popen(MUSIC_PATH)
                time.sleep(3)
            keyboard.press_and_release('play/pause media')
            print("音乐播放已启动")
        except Exception as e:
            print(f"播放失败：{str(e)}")

    def handle_forward(self):
        if self._check_music_process():
            self.next_track()
        else:
            self.ppt_next_slide()

    def handle_backward(self):
        if self._check_music_process():
            self.previous_track()
        else:
            self.ppt_prev_slide()

    def next_track(self):
        try:
            keyboard.press_and_release('next track')
            print("切换到下一曲目")
        except Exception as e:
            print(f"切歌失败：{str(e)}")

    def previous_track(self):
        try:
            keyboard.press_and_release('previous track')
            print("切换到上一曲目")
        except Exception as e:
            print(f"切歌失败：{str(e)}")

    def ppt_next_slide(self):
        if not ppt_app:
            print("警告: PowerPoint未正确初始化")
            return
        try:
            if ppt_app.Presentations.Count > 0:
                current_slide = ppt_app.ActiveWindow.View.Slide.SlideIndex
                if current_slide < ppt_app.ActivePresentation.Slides.Count:
                    ppt_app.ActiveWindow.View.GotoSlide(current_slide + 1)
                    print(f"切换到第 {current_slide + 1} 页")
        except Exception as e:
            print(f"PPT翻页失败：{str(e)}")

    def ppt_prev_slide(self):
        if not ppt_app:
            print("警告: PowerPoint未正确初始化")
            return
        try:
            if ppt_app.Presentations.Count > 0:
                current_slide = ppt_app.ActiveWindow.View.Slide.SlideIndex
                if current_slide > 1:
                    ppt_app.ActiveWindow.View.GotoSlide(current_slide - 1)
                    print(f"切换到第 {current_slide - 1} 页")
        except Exception as e:
            print(f"PPT翻页失败：{str(e)}")

    def volume_up(self):
        current_vol = volume_ctl.GetMasterVolumeLevelScalar()
        new_vol = min(round(current_vol + 0.1, 1), 1.0)
        volume_ctl.SetMasterVolumeLevelScalar(new_vol, None)
        print(f"音量已升至：{new_vol * 100}%")

    def volume_down(self):
        current_vol = volume_ctl.GetMasterVolumeLevelScalar()
        new_vol = max(round(current_vol - 0.1, 1), 0.0)
        volume_ctl.SetMasterVolumeLevelScalar(new_vol, None)
        print(f"音量已降至：{new_vol * 100}%")

    def handle_gesture(self, gesture):
        if gesture is not None:
            if gesture == gesture_labels["pause"]:
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