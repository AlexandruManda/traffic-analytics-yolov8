
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util import get_class_color, estimatedSpeed
from ultralytics import YOLO
import cv2
import cvzone
import math
import torch
from deep_sort_realtime.deepsort_tracker import DeepSort


class DeepSortTracker:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = self.load_model()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)
        self.class_name_dict = self.model.model.names
        self.video_path = os.path.join(
            self.current_dir, 'assets', 'videos', '2.mp4')
        self.mask_path = os.path.join(
            self.current_dir, 'assets', 'Images', 'mask.png')
        self.capture_index = self.video_path
        self.coordinatesDict = {}
        self.image_mask = cv2.imread(self.mask_path)
        self.tracker = self.init_tracker()

    def load_model(self):
        model_path = os.path.join(
            self.current_dir, 'runs', 'detect', 'train-v2', 'weights', 'best.pt')
        model = YOLO(model=model_path)
        model.fuse()
        return model

    def init_tracker(self):
        return DeepSort(
            max_iou_distance=0.7,
            max_age=5,
            n_init=3,
            nms_max_overlap=3.0,
            max_cosine_distance=0.2)

    def __call__(self):
        cap = cv2.VideoCapture(self.capture_index)
        while True:
            ret, img = cap.read()
            if not ret:
                print(
                    f"Failed to open video file with path {self.capture_index}")
                return
            assert ret
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            img_region = cv2.bitwise_and(img, self.image_mask)

            results = self.model.predict(img_region)
            detections = list()
            for r in results:
                boxes = r.boxes.cpu().numpy()
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    w, h = x2 - x1, y2 - y1
                    bbox = (x1, y1, w, h)
                    # Confidence
                    conf = math.ceil((box.conf[0]*100))/100

                    # Class Name
                    cls = int(box.cls[0])
                    if (conf > 0.3):
                        detections.append(([x1, y1, w, h], conf, cls))
                        currentClass = self.class_name_dict[cls]

            tracks = self.tracker.update_tracks(detections, frame=img)
            for track in tracks:
                if not track.is_confirmed():
                    continue
                track_id = track.track_id

                bbox = track.to_ltrb()
                x1, y1, x2, y2 = int(bbox[0]), int(
                    bbox[1]), int(bbox[2]), int(bbox[3])
                w, h = x2 - x1, y2 - y1

                co_ord = [x1, y1]

                if track_id not in self.coordinatesDict:
                    self.coordinatesDict[track_id] = co_ord
                else:
                    if len(self.coordinatesDict[track_id]) > 2:
                        del self.coordinatesDict[track_id][-3:-1]
                    self.coordinatesDict[track_id].append(co_ord[0])
                    self.coordinatesDict[track_id].append(co_ord[1])
                estimatedSpeedValue = 0
                if len(self.coordinatesDict[track_id]) > 2:
                    location1 = [self.coordinatesDict[track_id]
                                 [0], self.coordinatesDict[track_id][2]]
                    location2 = [self.coordinatesDict[track_id]
                                 [1], self.coordinatesDict[track_id][3]]
                    estimatedSpeedValue = estimatedSpeed(location1, location2)

                cls = track.get_det_class()
                currentClass = self.class_name_dict[cls]
                clsColor = get_class_color(currentClass)

                cvzone.cornerRect(img, (x1, y1, w, h), l=9,
                                  t=1, rt=2, colorR=clsColor, colorC=clsColor)

                cvzone.putTextRect(
                    img,
                    text=f"{self.class_name_dict[cls]} {estimatedSpeedValue} km/h",
                    pos=(max(0, x1), max(35, y1)),
                    colorR=clsColor,
                    scale=1,
                    thickness=1,
                    offset=2)

                cx, cy = x1+w//2, y1+h//2

                cv2.circle(img, (cx, cy), radius=5,
                           color=clsColor, thickness=cv2.FILLED)

            cv2.imshow("yolov8", img)
            if (cv2.waitKey(30) == 27):
                break


if __name__ == "__main__":
    tracker = DeepSortTracker()
    tracker()
