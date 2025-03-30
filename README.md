# SGMS

多场景手势智能交互控制系统（Multi-Scenario Intelligent Gesture Recognition Control System）

团队成员:[Future-Elite](https://github.com/Future-Elite),[tghrdwadhaihfoiw](https://github.com/tghrdwadhaihfoiw),[666lih](https://github.com/666lih),[Fengshuo123456](https://github.com/Fengshuo123456)

## 目录
- [项目背景](#项目背景)
- [项目需求](#项目需求)
- [项目设计](#项目设计)
- [安装](#安装)


## 项目背景

随着人工智能和计算机视觉技术的发展，手势识别作为自然交互方式，正逐步渗透到智能家居、医疗康复、教育培训、娱乐等领域。当前市场对非接触式交互需求激增，尤其在5G网络普及下，实时手势控制成为提升用户体验的核心技术方向。

本项目旨在开发一款基于电脑端的低成本手势识别系统，通过普通摄像头实现手势采集与识别，解决传统交互方式（如触控屏、鼠标）在特定场景（如湿手操作、沉浸式交互）中的局限性。

## 项目需求

系统需兼容图片（单张/批量）、视频文件及实时摄像头流三种输入方式，确保适应不同场景需求（如静态分析、动态追踪）。
摄像头输入需实现低延迟处理（如基于Mediapipe的实时关键点检测框架），并具备抗干扰能力（如光线变化、背景噪声）。  

手部区域检测采用深度学习模型（YOLO+Mediapipe）快速定位画面中的手部区域，区分左右手并输出边界框坐标。
关键点提取基于21个手部关键点（Mediapipe模型），实现手势的空间位置与姿态解析，支持手势动态追踪。

静态手势识别：

  支持常见手势分类（如石头、剪刀、布，或PAJ7620定义的9种基础动作），输出类别标签及置信度。  
  
动态手势识别：

  通过时序分析（如Android的GestureDetector滑动/长按检测）或双目视觉空间轨迹追踪，识别连续动作（如挥手、画圈）。  

算法优化：

  提供参数调节接口（如置信度阈值、IoU阈值），支持模型切换（YOLOv5至v8性能对比）以平衡速度与精度。


## 项目设计

1.系统架构图

![image](https://github.com/user-attachments/assets/3ef6a24a-aadd-4937-a1e1-681b295fff66)
![image](https://github.com/user-attachments/assets/54a15095-3e56-4ea0-a714-09cd8f7322bb)

2.核心数据流设计

![image](https://github.com/user-attachments/assets/8cc27c24-4be1-4ad9-be9e-5e47aa30a450)
![image](https://github.com/user-attachments/assets/4e9ac78a-b98b-4a51-9b8d-8fa9bf790049)

## 安装
### 前置要求
python>=3.9

### Setup
```bash
git clone [https://github.com/Future-Elite/SGMS]
cd [project-name]
pip install -r requirements.txt
