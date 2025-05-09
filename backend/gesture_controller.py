import requests
import time


gesture_labels = {
        "start": 0,
        "pause": 1,
        "forward": 2,
        "backward": 3,
        "high": 4,
        "low": 5
    }


def action_0():
    print("执行操作 0")


def action_1():
    print("执行操作 1")


def action_2():
    print("执行操作 2")


def action_3():
    print("执行操作 3")


def action_4():
    print("执行操作 4")


def action_5():
    print("执行操作 5")


def get_gesture_from_flask():
    try:
        response = requests.get('http://localhost:5000/result')
        if response.status_code == 200:
            data = response.json()
            return gesture_labels.get(data, None)
        else:
            return None
    except Exception as e:
        print(f"请求异常：{e}")
        return None


class GestureController:
    def __init__(self):
        self.actions = {
            0: action_0,
            1: action_1,
            2: action_2,
            3: action_3,
            4: action_4,
            5: action_5
        }

    # 调用对应的操作函数
    def handle_gesture(self, gesture):
        # TODO: 添加手势处理逻辑

        if gesture is not None and gesture in self.actions:
            self.actions[gesture]()
        else:
            print("无效的手势")

    # 监听手势的主循环
    def start_listening(self):
        while True:
            gesture = get_gesture_from_flask()
            if gesture is not None:
                self.handle_gesture(gesture)
            time.sleep(1)


# 启动手势控制器并监听手势
if __name__ == '__main__':
    controller = GestureController()
    controller.start_listening()
