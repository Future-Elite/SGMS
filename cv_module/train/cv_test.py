import cv2
import mediapipe as mp

from ultralytics import YOLO

# ========== 初始化MediaPipe ==========
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands_detector = mp_hands.Hands(static_image_mode=True,
                                model_complexity=1,
                                max_num_hands=1,
                                min_detection_confidence=0.3,
                                min_tracking_confidence=0.5)

model = YOLO('../ptfiles/yolo11n-cls.pt')


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 转换颜色 BGR -> RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 处理图像
        results = hands_detector.process(image_rgb)

        # 绘制骨架到黑图上
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                )

        # 使用YOLO模型进行检测
        results = model.predict(frame, conf=0.5, show=True)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
