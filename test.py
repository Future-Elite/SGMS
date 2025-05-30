import cv2


def check_camera():
    test = cv2.VideoCapture(0)
    if not test.isOpened():
        raise RuntimeError("Camera already in use or not available")
    test.release()


check_camera()
