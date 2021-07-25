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

        # Write one frame
        self._captureManager.enterFrame()
        frame = self._captureManager.frame

        if not pipeline is None:
            assert(type(pipeline(frame)) == np.ndarray)

        self._captureManager.exitFrame(frame)

    def addKeyCallback(self, key, func):
        self._windowManager.keyPressCallbacks[key] = func


    def addCloseCallback(self, key=113):
        self.addKeyCallback(key, lambda x : self.close())
        return self


    def run(self):
        self._windowManager.createWindow()

        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()

            frame = self._captureManager.frame

            if not self.pipeline is None:
                frame = self.pipeline(frame)

            self._windowManager.show(frame)
            self._captureManager.exitFrame(frame)

            self._windowManager.proccessKeyEvents()


    def writeVideo(self, filename):
        self._captureManager.startWritingVideo(filename)


    def close(self):
        self._windowManager.close()
        self._captureManager.close()


if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    cam = CameraManager('TestWindow', capture).addCloseCallback()
    cam.run()