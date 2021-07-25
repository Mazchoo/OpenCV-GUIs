import cv2
import pdb

class WindowManager:

    def __init__(self, windowName, keyPressCallbacks={}, mouseCallback=None):
        '''
            Create an openCV window that has callbacks
            
            mouseCallback is a function to mouse events
                f(event, x, y, flags, param)
            
            keyPressCallbacks is a dictionary of single parameter functions
            The key should be the number code of the actual key that was pressed
                { k1: def: f(key), k2: def: f(key) ... }
        '''

        self.mouseCallback = mouseCallback
        self.keyPressCallbacks = keyPressCallbacks
        
        self._windowName = windowName
        self._isWindowCreated = False
    
    
    @property
    def isWindowCreated(self):
        return self._isWindowCreated
    
    
    def createWindow(self):
        cv2.namedWindow(self._windowName)
        if self.mouseCallback:
            cv2.setMouseCallback(self._windowName, self.mouseCallback)
        self._isWindowCreated = True
    
    
    def show(self, frame):
        if not frame is None:
            cv2.imshow(self._windowName, frame)
    
    
    def close(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False
    
    
    def proccessKeyEvents(self):
        keycode = cv2.waitKey(1)

        if self.keyPressCallbacks and keycode!=-1:
            keycode &= 0xFF
            try:
                if keycode in self.keyPressCallbacks:
                    self.keyPressCallbacks[keycode](keycode)
            except Exception as e:
                print('The function call for key {} failed.'.format(keycode))
                print(e)