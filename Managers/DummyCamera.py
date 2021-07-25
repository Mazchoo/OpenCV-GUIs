import cv2
import time

class DummyCapture: # Could make an abstract base class of a capture object
    def __init__(self, nrImages=1, delay=1):
        cap = cv2.VideoCapture(0)
        self.frames = []
        self.state = 0
        self.nrImages = nrImages
        
        for i in range(nrImages):
            time.sleep(delay)
            success, frame = cap.read()

            if not success:
                print('Reading capture failed!')
                cap.release()
                return
        
            self.frames.append(frame)
    
    
    def grab(self):
        self.state += 1
        return True, self.frames[self.state % self.nrImages]
    
    
    def retrieve(self):
        return True, self.frames[self.state % self.nrImages]

    
    def read(self):
        return self.retrieve()

    
    def release(self, *args, **kwargs):
        pass