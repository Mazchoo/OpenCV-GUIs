import cv2
import numpy as np
import time

class CaptureManager:

    def __init__(self, capture):

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFileName = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._frameElapsed = 0
        self._fpsEstimate = None


    @property
    def channel(self):
        return self._channel


    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None


    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame


    @property
    def isWritingImage(self):
        return self._imageFileName is not None


    @property
    def isWritingVideo(self):
        return self._videoFilename is not None


    def enterFrame(self):
        assert not self._enteredFrame, 'Entering a frame while old instance is still running.'

        if self._capture is not None:
            self._enteredFrame = self._capture.grab()


    def exitFrame(self, frame):
        if frame is None:
            self.enteredFrame = False
            return

        if self._frameElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime + 1e-7
            self._fpsEstimate = self._frameElapsed / timeElapsed
        self._frameElapsed += 1

        if self.isWritingImage:
            cv2.imwrite(self._imageFilename, frame)
            self._imageFilename = None

        self._writeVideoFrame()
        self._frame = None
        self._enteredFrame = False


    def writeImage(self, filename):
        self._imageFilename = filename


    def startWritingVideo(self, filename, encoding=cv2.VideoWriter_fourcc('I', '4', '2', '0')):
        self._videoFilename = filename
        self._videoEncoding = encoding


    def stopWritingVideo(self):
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None


    def _writeVideoFrame(self):

        if not self.isWritingVideo:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)

            if fps == 0.:
                if self._frameElapsed < 20:
                    return
                else:
                    fps = self._fpsEstimate

                size= (int(self._capture.get(
                           cv2.CAP_PROP_FRAME_WIDTH)),
                       int(self._capture.get(
                           cv2.CAP_PROP_FRAME_HEIGHT)))

                self._videoWriter = cv2.VideoWriter(
                        self._videoFilename, self._videoEncoding, fps, size
                )

        self._videoWriter.write(self._frame)


    def close(self):
        self._capture.release()


if __name__ == '__main__':
    manager = CaptureManager(cv2.VideoCapture(0))
