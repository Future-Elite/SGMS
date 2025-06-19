import cv2
import base64
import requests
import uuid
import sys
import os


def image_to_base64(image_path):
    if not os.path.exists(image_path):
        print(f"错误：文件不存在：{image_path}")
        sys.exit(1)

    img = cv2.imread(image_path)
    if img is None:
        print(f"错误：无法读取图像：{image_path}")
        sys.exit(1)

    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64


def send_recognition_request(image_path, server_url="http://localhost:5000/api/recognize"):
    img_base64 = image_to_base64(image_path)
    payload = {
        "frame_data": img_base64,
        "session_id": str(uuid.uuid4())
    }

    try:
        response = requests.post(server_url, json=payload)
        print("状态码:", response.status_code)
        print("返回结果:", response.json())
    except requests.exceptions.RequestException as e:
        print("请求失败:", e)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: python recognize_client.py <image_path> [server_url]")
        sys.exit(1)

    image_path = sys.argv[1]
    send_recognition_request(image_path)
