# SGMS

多场景手势智能交互控制系统（Multi-Scenario Intelligent Gesture Recognition Control System）

团队成员:[Future-Elite](https://github.com/Future-Elite),[tghrdwadhaihfoiw](https://github.com/tghrdwadhaihfoiw),[666lih](https://github.com/666lih),[Fengshuo123456](https://github.com/Fengshuo123456)

## 目录
- [项目背景](#项目背景)
- [项目需求](#项目需求)
- [项目设计](#项目设计)
- [安装](#安装)


## 项目背景
随着人工智能技术的迅猛发展，手势识别作为人机交互的重要方式，正在医疗健康、教育培训、智能家居、工业控制等领域展现出巨大潜力。多场景手势智能交互控制系统（SGMS）是基于计算机视觉技术，通过摄像头对智能设备实现自然、直观的手势控制。

本项目针对传统交互方式在特定场景中的局限性，开发了一套低成本、高性能的手势识别系统。其中AI模块的核心作用为：自适应周围环境（模型只关注手部关键点信息），精准的手势识别（采用预训练策略），手势-控制功能的映射。

## 项目需求
系统需实时视频处理（主界面）利用OpenCV高效采集和处理1080P视频流，实现30FPS高帧率显示。手部区域检测采用深度学习模型（YOLO+Mediapipe）快速定位画面中的手部区域，区分左右手并输出边界框坐标。关键点提取基于21个手部关键点（Mediapipe模型），实现手势的空间位置与姿态解析，支持手势动态追踪。


手部区域检测​​：

  采用MediaPipe BlazePalm模型（非YOLO）进行毫秒级手部定位

​​关键点提取与追踪​​：

  基于MediaPipe 21点手部骨骼模型提取空间坐标

  
## 项目设计

1.系统总体结构

![image](https://github.com/user-attachments/assets/376782d0-130c-4e83-aecb-62aaf1c3e27d)


2.业务模块与AI模块交互图

![image](https://github.com/user-attachments/assets/f46d0765-9837-4e97-ae66-b4585d89845d)

3.智能模块处理逻辑
![image](https://github.com/user-attachments/assets/2caf75b3-e26e-474e-9b10-ed19bc5c0af7)


## 安装
### 前置要求
python>=3.9

### Setup
```bash
git clone [https://github.com/Future-Elite/SGMS]
conda create -n SGMS
conda activate SGMS
cd [project-name]
pip install -r requirements.txt
```
### 演示视频
见demo/demo.mp4
