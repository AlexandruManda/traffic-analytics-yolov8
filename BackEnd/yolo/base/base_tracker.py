
from abc import ABC, abstractmethod
import re

class BaseTracker(ABC):
    def __init__(self, source=0,model_name="yolo-highway-v2.pt"):
        """
        Initializes the BaseTracker.

        Args:
            source (str or int): The path to the video source or camera index. Default is 0 (camera).
        """
        self.source = source
        self.model_name=model_name

    @abstractmethod
    def load_model(self):
        """
        Loads the model.
        """
        pass

    @abstractmethod
    def process_frame(self):
        """
        Processes a single frame of the video stream.
        """
        pass

    @abstractmethod
    def show(self):
        """
        Runs the tracking process and displays the processed video frames on the screen.
        """
        pass

    def __call__(self):
        """
        Runs the tracking process.
        """
        pass
    def is_youtube_url(self,url):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )

        youtube_pattern = re.compile(youtube_regex)

        if youtube_pattern.match(url) is not None:
            return True
        else:
            return False
