import os
import shutil
import random

# 配置
dataset_dir = '../datasets/dataset_a/train'  # 原始数据集路径
output_dir = '../../datasets/dataset_a_split'  # 输出路径
train_ratio = 0.8  # 训练集比例

# 创建输出目录
for split in ['train', 'val']:
    split_path = os.path.join(output_dir, split)
    os.makedirs(split_path, exist_ok=True)

# 遍历每个类别
for class_name in os.listdir(dataset_dir):
    class_path = os.path.join(dataset_dir, class_name)
    if not os.path.isdir(class_path):
        continue

    images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    random.shuffle(images)

    train_num = int(len(images) * train_ratio)
    train_images = images[:train_num]
    val_images = images[train_num:]

    # 创建类别目录
    train_class_dir = os.path.join(output_dir, 'train', class_name)
    val_class_dir = os.path.join(output_dir, 'val', class_name)
    os.makedirs(train_class_dir, exist_ok=True)
    os.makedirs(val_class_dir, exist_ok=True)

    # 复制文件
    for img in train_images:
        shutil.copy(os.path.join(class_path, img), os.path.join(train_class_dir, img))
    for img in val_images:
        shutil.copy(os.path.join(class_path, img), os.path.join(val_class_dir, img))

    print(f"{class_name}: 训练 {len(train_images)} 张，验证 {len(val_images)} 张")

print("划分完成！")
