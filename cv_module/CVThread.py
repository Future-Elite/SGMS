import json
import os.path
import cv2
import numpy as np
import torch
from PySide6.QtCore import QThread, Signal
from pathlib import Path
from frontend.utils import pipe, glo
from backend.result_updater import ResultUpdater
from ultralytics.data import load_inference_source
from ultralytics.data.augment import classify_transforms, LetterBox
from ultralytics.engine.predictor import STREAM_WARNING
from ultralytics.engine.results import Results
from ultralytics.nn.autobackend import AutoBackend
from ultralytics.utils import callbacks, ops, LOGGER
from collections import defaultdict
from ultralytics.utils.checks import check_imgsz
from ultralytics.utils.torch_utils import select_device
from concurrent.futures import ThreadPoolExecutor
import mediapipe as mp


class CVThread(QThread):
    send_output = Signal(np.ndarray)
    send_msg = Signal(str)

    def __init__(self):
        super(CVThread, self).__init__()

        self.uploader = ResultUpdater('http://localhost:5000/result')
        self.model_name = 'cv_module/ptfiles/yolo11s-cls.pt'
        self.hands = None
        self.ori_img = None
        self.results = None
        self.source = None
        self.stop_dtc = True
        self.is_continue = True
        self.iou_thres = 0.45
        self.conf_thres = 0.25
        self.labels_dict = {}
        self.parent_workpath = None
        self.executor = ThreadPoolExecutor(max_workers=1)

        # mediapipe 参数设置
        self.mp_pose = None
        self.mp_pose_results = None

        # YOLO 参数设置
        self.model = None
        self.imgsz = 640
        self.device = ''
        self.dataset = None
        self.source_type = None
        self.task = 'classify'
        self.dnn = False
        self.half = False
        self.crop_fraction = 1.0
        self.done_warmup = False
        self.batch = None
        self.classes = None  # 指定检测类别
        self.line_thickness = 4
        self.plotted_img = None
        self.callbacks = defaultdict(list, callbacks.default_callbacks)  # add callbacks
        callbacks.add_integration_callbacks(self)

    def run(self):
        if not self.model:
            self.send_msg.emit("Loading model: {}".format(os.path.basename(self.model_name)))
            self.setup_model(self.model_name)
        self.setup_source('http://localhost:5000/stream')
        self.detect()

    @torch.no_grad()
    def detect(self):
        # warmup model
        if not self.done_warmup:
            self.model.warmup(imgsz=(1 if self.model.pt or self.model.triton else self.dataset.bs, 3, *self.imgsz))
            self.done_warmup = True
        self.seen, self.windows, self.dt, self.batch = 0, [], (ops.Profile(), ops.Profile(), ops.Profile()), None
        datasets = iter(self.dataset)
        count = 0

        while True:
            if self.stop_dtc:
                self.send_msg.emit('Stop Detection')
                self.dataset.running = False
                # 判断self.dataset里面是否有threads
                if hasattr(self.dataset, 'threads'):
                    for thread in self.dataset.threads:
                        if thread.is_alive():
                            thread.join(timeout=1)
                if hasattr(self.dataset, 'caps'):
                    for cap in self.dataset.caps:
                        try:
                            cap.release()
                        except Exception as e:
                            LOGGER.warning(f"WARNING Could not release VideoCapture object: {e}")
                cv2.destroyAllWindows()
                break
            if self.is_continue:
                self.batch = next(datasets)
                path, im0s, s = self.batch
                self.ori_img = im0s.copy()
                has_hand = False
                for i, image in enumerate(im0s):
                    black_img = np.zeros(im0s[i].shape, dtype=np.uint8)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = self.hands.process(image)
                    if results.multi_hand_landmarks:
                        has_hand = True
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        for oneHand in results.multi_hand_landmarks:
                            mp.solutions.drawing_utils.draw_landmarks(image, oneHand,
                                                                      mp.solutions.hands.HAND_CONNECTIONS)
                            mp.solutions.drawing_utils.draw_landmarks(
                                black_img, oneHand, mp.solutions.hands.HAND_CONNECTIONS,
                            )
                        self.ori_img[i] = image
                        im0s[i] = black_img

                count += 1

                with self.dt[0]:
                    im = self.preprocess(im0s)
                with self.dt[1]:
                    preds = self.inference(im)
                with self.dt[2]:
                    self.results = self.postprocess(preds, im, im0s)

                n = len(im0s)
                for i in range(n):
                    self.seen += 1
                    self.results[i].speed = {
                        "preprocess": self.dt[0].dt * 1e3 / n,
                        "inference": self.dt[1].dt * 1e3 / n,
                        "postprocess": self.dt[2].dt * 1e3 / n,
                    }

                    p, im0 = path[i], None if self.source_type.tensor else im0s[i].copy()
                    p = Path(p)

                    label_str = self.write_results(i, self.results, (p, im, im0))  # labels   /// original :s +=
                    if not has_hand:
                        label_str = 'no detections'

                    class_nums = 0
                    target_nums = 0
                    self.labels_dict = {}
                    if 'no detections' in label_str:
                        pass
                    else:
                        for each_target in label_str.split(',')[:-1]:
                            num_labelname = list(each_target.split(' '))
                            nums = 0
                            label_name = ""
                            for each in range(len(num_labelname)):
                                if num_labelname[each].isdigit() and each != len(num_labelname) - 1:
                                    nums = num_labelname[each]
                                elif len(num_labelname[each]):
                                    label_name += num_labelname[each] + " "
                            target_nums += int(nums)
                            class_nums += 1
                            if label_name in self.labels_dict:
                                self.labels_dict[label_name] += int(nums)
                            else:  # 第一次出现的类别
                                self.labels_dict[label_name] = int(nums)

                    if has_hand:
                        self.send_output.emit(self.plotted_img)
                        pipe.frame = self.plotted_img
                    else:
                        self.send_output.emit(self.ori_img[0])
                        pipe.frame = self.ori_img[0]

                    self.uploader.submit(self.labels_dict)  # 提交最新结果

                    try:
                        with open('data/config/tmp.json', "w") as f:
                            json.dump(self.labels_dict, f)
                        os.replace('data/config/tmp.json', 'data/config/res.json')
                    except Exception as e:
                        pass

    def setup_model(self, model, verbose=True):
        self.model = AutoBackend(
            weights=model or self.model,
            device=select_device(self.device, verbose=verbose),
            dnn=self.dnn,
            fp16=self.half,
            fuse=True,
            verbose=verbose
        )

        self.device = self.model.device
        self.half = self.model.fp16
        self.model.eval()

        # 加入mediapipe
        self.mp_pose = mp.solutions.hands
        self.hands = self.mp_pose.Hands(True, 1, 1, 0.5, 0.5)

    def setup_source(self, source):
        self.imgsz = check_imgsz(self.imgsz, stride=self.model.stride, min_dim=2)  # check image size
        self.transforms = (
            getattr(
                self.model.model,
                "transforms",
                classify_transforms(self.imgsz[0], crop_fraction=self.crop_fraction),
            )
            if self.task == "classify"
            else None
        )
        self.dataset = load_inference_source(
            source=source,
            batch=1,
            vid_stride=1,
            buffer=False
        )

        self.source_type = self.dataset.source_type
        if not getattr(self, "stream", True) and (
                self.source_type.stream
                or self.source_type.screenshot
                or len(self.dataset) > 1000  # many images
                or any(getattr(self.dataset, "video_flag", [False]))
        ):  # videos
            LOGGER.warning(STREAM_WARNING)

    def postprocess(self, preds, img, orig_imgs):
        if not isinstance(orig_imgs, list):
            orig_imgs = ops.convert_torch2numpy_batch(orig_imgs)

        results = []


        a = preds[0].cpu().numpy().tolist()[0]
        class_index = a.index(max(a))
        conf = a[class_index]
        preds = [torch.Tensor([[0, 0, 1, 1, conf, class_index]])]

        for i, pred in enumerate(preds):
            orig_img = orig_imgs[i]
            pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], orig_img.shape)
            img_path = self.batch[0][i]
            results.append(Results(orig_img, path=img_path, names=self.model.names, boxes=pred))

        return results

    def preprocess(self, im):
        not_tensor = not isinstance(im, torch.Tensor)
        if not_tensor:
            im = np.stack(self.pre_transform(im))
            im = im[..., ::-1].transpose((0, 3, 1, 2))
            im = np.ascontiguousarray(im)
            im = torch.from_numpy(im)

        im = im.to(self.device)
        im = im.half() if self.model.fp16 else im.float()
        if not_tensor:
            im /= 255
        return im

    def inference(self, im, *args, **kwargs):
        return self.model(im, augment=False, visualize=False, embed=False, *args, **kwargs)

    def pre_transform(self, im):
        same_shapes = all(x.shape == im[0].shape for x in im)
        letterbox = LetterBox(self.imgsz, auto=same_shapes and self.model.pt, stride=self.model.stride)
        return [letterbox(image=x) for x in im]

    def write_results(self, idx, results, batch):
        p, im, _ = batch
        log_string = ""
        if len(im.shape) == 3:
            im = im[None]

        result = results[idx]
        log_string += result.verbose()
        result = results[idx]

        result.orig_img = self.ori_img[idx]

        plot_args = {
            "line_width": self.line_thickness,
            "boxes": True,
            "conf": True,
            "labels": True,
        }
        self.plotted_img = result.plot(**plot_args)
        return log_string
