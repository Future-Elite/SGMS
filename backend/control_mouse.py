import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from collections import deque

# 超参数配置
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,  # 简化模型提升速度
    min_detection_confidence=0.5,
    min_tracking_confidence=0.4)  # 降低跟踪置信阈值

# 显示参数
screen_w, screen_h = pyautogui.size()

# 视频流配置
cap = cv2.VideoCapture(0)

# 灵敏度优化参数
frame_margin = 30  # 缩小无效区域
smooth_window = 3  # 缩短平滑窗口
dynamic_smoothing = True  # 启用动态平滑

# 运动追踪优化
pyautogui.PAUSE = 0
velocity_queue = deque(maxlen=5)
coord_history = deque(maxlen=smooth_window)


def adaptive_smooth(new_x, new_y):
    """动态平滑算法：根据移动速度自动调节平滑强度"""
    global coord_history

    # 计算移动速度
    if coord_history:
        prev_x, prev_y = coord_history[-1]
        velocity = np.hypot(new_x - prev_x, new_y - prev_y)
        velocity_queue.append(velocity)
    else:
        velocity = 0

    # 动态平滑系数
    avg_velocity = np.mean(velocity_queue) if velocity_queue else 0
    alpha = max(0.3, 1 - avg_velocity / 200)  # 速度越快平滑系数越小

    # 指数平滑
    if coord_history:
        last_x, last_y = coord_history[-1]
        smoothed_x = new_x * (1 - alpha) + last_x * alpha
        smoothed_y = new_y * (1 - alpha) + last_y * alpha
    else:
        smoothed_x, smoothed_y = new_x, new_y

    coord_history.append((smoothed_x, smoothed_y))
    return np.mean([x for x, y in coord_history]), np.mean([y for x, y in coord_history])


while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    # 高效图像处理
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 实时处理每帧
    results = hands.process(rgb_frame)

    # 绘制交互区域
    h, w = frame.shape[:2]
    cv2.rectangle(frame,
                  (frame_margin, frame_margin),
                  (w - frame_margin, h - frame_margin),
                  (0, 255, 0), 1)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # 获取高精度坐标
        cx = int(index_tip.x * w)
        cy = int(index_tip.y * h)

        # 在有效区域内处理
        if frame_margin < cx < w - frame_margin and frame_margin < cy < h - frame_margin:
            # 非线性坐标映射（中心区域灵敏，边缘快速移动）
            x_ratio = (cx - frame_margin) / (w - 2 * frame_margin)
            y_ratio = (cy - frame_margin) / (h - 2 * frame_margin)

            # 二次曲线映射
            mapped_x = screen_w * (x_ratio ** 1.3)
            mapped_y = screen_h * (y_ratio ** 1.3)

            # 动态平滑处理
            final_x, final_y = adaptive_smooth(mapped_x, mapped_y)

            # 执行低延迟移动
            pyautogui.moveTo(
                int(screen_w - final_x),
                int(final_y),
                duration=0.001,  # 最小化移动耗时
                _pause=False
            )

            # 实时反馈
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
            cv2.line(frame, (cx, cy), (cx, cy), (255, 255, 0), 15)

    # 优化显示
    cv2.imshow('Precision Tracker', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
