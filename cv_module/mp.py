import os
import cv2
import numpy as np
import mediapipe as mp
from tqdm import tqdm

# ========== 配置路径 ==========
SOURCE_DIR = '../datasets/dataset_a_split/val'  # 原始图像数据集路径（按类别分类）
OUTPUT_DIR = '../datasets/dataset_a_split_mp/val'  # 输出图像数据集路径

# ========== 创建输出目录 ==========
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== 初始化MediaPipe ==========
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands_detector = mp_hands.Hands(static_image_mode=True,
                                model_complexity=1,
                                max_num_hands=1,
                                min_detection_confidence=0.3,
                                min_tracking_confidence=0.5)

# ========== 遍历数据集 ==========
for class_name in os.listdir(SOURCE_DIR):
    class_input_path = os.path.join(SOURCE_DIR, class_name)
    class_output_path = os.path.join(OUTPUT_DIR, class_name)

    if not os.path.isdir(class_input_path):
        continue

    os.makedirs(class_output_path, exist_ok=True)

    for img_name in tqdm(os.listdir(class_input_path), desc=f"Processing {class_name}"):
        if not img_name.lower().endswith(('.jpg', '.png', '.jpeg')):
            continue

        img_path = os.path.join(class_input_path, img_name)
        output_path = os.path.join(class_output_path, img_name)

        # 读取图片
        image = cv2.imread(img_path)
        if image is None:
            continue

        # 创建黑色背景
        black_img = np.zeros_like(image)

        # 转换颜色 BGR -> RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 处理图像
        results = hands_detector.process(image_rgb)

        # 绘制骨架到黑图上
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    black_img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

            # 保存替换图像
            cv2.imwrite(output_path, black_img)



# 释放资源
hands_detector.close()
print("处理完成，保存至:", OUTPUT_DIR)
