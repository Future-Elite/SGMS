import cv2
import base64
import requests
import uuid

# 读取本地图片
img = cv2.imread(input('Image Path:'))

# 编码为 JPEG 格式
_, buffer = cv2.imencode('.jpg', img)

# 转为 base64
img_base64 = base64.b64encode(buffer).decode('utf-8')

# 准备请求数据
payload = {
    "frame_data": img_base64,
    "session_id": str(uuid.uuid4())
}

# 发送 POST 请求
response = requests.post("http://localhost:5000/api/recognize", json=payload)

# 打印结果
print(response.json())
