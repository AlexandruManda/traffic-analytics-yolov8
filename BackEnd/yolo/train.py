from roboflow import Roboflow
from ultralytics import YOLO
import torch,os
import argparse

class YOLOTrainer:
    def __init__(self, project="highway-cars-object-detection", version=2, device=None):
    
        yolo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dataset_path = os.path.join(yolo_dir,"yolo","datasets",f"{project}-{version}")
        self.device = device if device else '0' if torch.cuda.is_available() else 'cpu'
        self.model = None

    def load_model(self, weights_path):
        self.model = YOLO(model=weights_path)


    def train(self,**kwargs):
        if self.model is None:
            self.load_model(kwargs.get('weights_path'))
            
        data_path = f"{self.dataset_path}\data.yaml"

        self.model.train(
            data=data_path,
            epochs=kwargs.get('epochs'),
            imgsz=kwargs.get('imgsz'),
            save=kwargs.get('save'),
            cache=kwargs.get('cache'),
            device=kwargs.get('device'),
            workers=kwargs.get('workers'),
            batch=kwargs.get('batch')
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=25)
    parser.add_argument('--weights_path', type=str, default='./models/yolov8m.pt')
    parser.add_argument('--imgsz', type=int, default=640)
    parser.add_argument('--save', type=bool, default=True)
    parser.add_argument('--cache', type=bool, default=False)
    parser.add_argument('--device', type=str, default="cpu")
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--batch', type=int, default=4)
    args = parser.parse_args()

    trainer = YOLOTrainer()
    trainer.train(**vars(args))
