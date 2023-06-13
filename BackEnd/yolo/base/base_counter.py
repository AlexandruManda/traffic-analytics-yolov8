
from abc import ABC, abstractmethod


class BaseCounter(ABC):
    def __init__(self, class_names_dict):
        self.class_names_dict = class_names_dict

  
    @abstractmethod
    def draw(self, frame):
        pass
       
    @abstractmethod
    def count(self, detections):  
        pass
