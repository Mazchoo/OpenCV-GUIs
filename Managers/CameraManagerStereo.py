import cv2
import numpy as np

from .CaptureManager import *
from .WindowManager import *

class CameraManagerStereo:

    def __init__(self, windowName, captures:list, pipeline,
                       keyPressCallbacks={}, mouseCallback=None):

        self._windowManager = WindowManager(
            windowName, keyPressCallbacks=keyPressCallbacks, mouseCallback=mouseCallback
        )
        self.captures = []
        for cap in captures:
            self.captures.append(CaptureManager(cap))

        self.pipeline = pipeline
        self.valid    = False

        try:
            frames = [] # This could be allocated here instead of appending

            for cap in self.captures:
                cap.enterFrame()
                frames.append(cap.frame)

            assert(type(pipeline(frames)) == np.ndarray)

            for cap, frame in zip(self.captures, frames): cap.exitFrame(frame)
            self.valid = True

        except Exception as e:
            print(e)
            for cap in self.captures: cap.exitFrame(None)
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
            frames = []

            for cap in self.captures:
                cap.enterFrame()
                frames.append(cap.frame)

            frame = self.pipeline(frames)

            self._windowManager.show(frame)
            for cap, frame in zip(self.captures, frames): cap.exitFrame(frame)

            self._windowManager.proccessKeyEvents()


    def close(self):
        self._windowManager.close()
        for cap in self.captures: cap.close()


    def addBasicButtons(self):
        pass
