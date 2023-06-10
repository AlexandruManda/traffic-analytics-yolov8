import os
import sys
import torch
import numpy as np
import cv2

from supervision.draw.color import ColorPalette
from supervision import BoxAnnotator, Detections
from ultralytics import YOLO
from time import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util import encode_mat_base64, resize_image, compress_image

class ObjectDetection:
    def __init__(self, source=0):
        self.source = source
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)
        self.model = self.load_model()
        self.class_names_dict = self.model.model.names
        self.box_annotator = BoxAnnotator(
            color=ColorPalette.default(), thickness=2, text_thickness=1, text_scale=0.5, text_padding=2)

    def load_model(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(
            current_dir, 'runs', 'detect', 'train-v2', 'weights', 'best.pt')
        model_path = os.path.join(current_dir, 'models', 'yolov8s.pt')
        model = YOLO(model=model_path)
        model.fuse()
        return model

    def get_model(self):
        return self.model

    def predict(self, frame):

        results = self.model(frame, verbose=False)

        return results

    def plot_bboxes(self, results, frame):
        xyxys = []
        confidences = []
        class_ids = []

        # Extract detections for person class
        for result in results[0]:
            class_id = result.boxes.cls.cpu().numpy().astype(int)
            # print(result.boxes)

            if class_id == 0:
                xyxys.append(result.boxes.xyxy.cpu().numpy())
                confidences.append(result.boxes.conf.cpu().numpy())
                class_ids.append(result.boxes.cls.cpu().numpy().astype(int))

        # Setup detections for visualization
        detections = Detections(
            xyxy=results[0].boxes.xyxy.cpu().numpy(),
            confidence=results[0].boxes.conf.cpu().numpy(),
            class_id=results[0].boxes.cls.cpu().numpy().astype(int),
        )

        # Format custom labels
        self.labels = [f"{self.class_names_dict[class_id]} {confidence:0.2f}"
                       for _, confidence, class_id, tracker_id
                       in detections]

        # Annotate and display frame
        frame = self.box_annotator.annotate(
            scene=frame, detections=detections, labels=self.labels)

        return frame

    def __call__(self):
        cap = cv2.VideoCapture(self.source)

        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:

            start_time = time()

            ret, frame = cap.read()
            assert ret

            results = self.predict(frame)
            frame = self.plot_bboxes(results, frame)

            end_time = time()
            fps = 1/np.round(end_time - start_time, 2)

            cv2.putText(frame, f'FPS: {int(fps)}', (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')
            # cv2.imshow("image",frame)
            # if cv2.waitKey(5) & 0xFF == 27:
            #     break
        # cap.release()
        # cv2.destroyAllWindows()

    def gen_image(self, frame):

        results = self.predict(frame)

        frame = self.plot_bboxes(results, frame)
        frame = resize_image(frame, 640, 640)
        frame = compress_image(frame, 70)

        return encode_mat_base64(frame)


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, 'assets', 'videos', '1.mp4')
    # video_path="https://www.youtube.com/watch?v=lPjevDc5G8E"
    detector = ObjectDetection(source=video_path)
    detector()
