import cv2
from threading import Thread, Lock

class objDetection:

    #threading properties
    stopped = True
    lock = None
    rectangles = []

    #properties
    cascade = None
    screenshot = None

    def __init__(self, model_file_path):
        #create thread lock
        self.lock = Lock()
        #load trained model
        self.cascade_willows = cv2.CascadeClassifier(model_file_path)

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        detect_thread = Thread(target=self.run)
        detect_thread.start()
    
    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if not self.screenshot is None:
                # do object detection
                rectangles = self.cascade_willows.detectMultiScale(self.screenshot)
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()

