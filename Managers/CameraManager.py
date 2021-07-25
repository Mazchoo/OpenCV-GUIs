import cv2
import numpy as np

from .CaptureManager import *
from .WindowManager import *

class CameraManager:

    def __init__(self, windowName, capture, pipeline=None, keyPressCallbacks={}, mouseCallback=None):
        self._windowManager = WindowManager(
            windowName, keyPressCallbacks=keyPressCallbacks, mouseCallback=mouseCallback
        )
        self._captureManager = CaptureManager(capture)
        self.pipeline = pipeline
        self.valid    = False

        try:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame

            if not pipeline is None:
                assert(type(pipeline(frame)) == np.ndarray)

            self._captureManager.exitFrame(frame)
            self.valid = True

        except Exception as e:
            print(e)
            self._captureManager.exitFrame(None)
            print('Error! Could not process one frame.')


    def addKeyCallback(self, key, func):
        self._windowManager.keyPressCallbacks[key] = func


    def addCloseCallback(self, key=113):
        self.addKeyCallback(key, lambda x : self.close())
        return self


    def run(self):
        if not self.valid: return
        self._windowManager.createWindow()

        while self._windowManager.isWindowCreated and self.valid:
            self._captureManager.enterFrame()

            frame = self._captureManager.frame

            if not self.pipeline is None:
                frame = self.pipeline(frame)

            self._windowManager.show(frame)
            self._captureManager.exitFrame(frame)

            self._windowManager.proccessKeyEvents()


    def close(self):
        self._windowManager.close()
        self._captureManager.close()


    def addBasicButtons(self):
        pass


if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    cam = CameraManager('TestWindow', capture).addCloseCallback()
    cam.run()