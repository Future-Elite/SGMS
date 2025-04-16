from ultralytics import YOLO


if __name__ == '__main__':

    # Load a model
    model = YOLO("yolo11n-cls.pt")

    # Train the model
    results = model.train(data="../datasets/dataset_a", cfg='./config.yaml')
