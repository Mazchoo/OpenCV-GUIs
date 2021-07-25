import cv2

window_name = 'DisplayWindow'


def onMouseEvent(event, x, y, flags, param):
    '''
        Events and flags can be used like bitwise operations
        They go in powers of 2 so the and operation is equivalent to
        event ==  cv2.EVENT_MOUSEMOVE + 
    '''
    if event == cv2.EVENT_LBUTTONDOWN:
        print('That was a left down')
    elif event == cv2.EVENT_LBUTTONUP:
        print('That was a left up')
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        print('That was a left click')
    elif event == cv2.EVENT_MOUSEMOVE:
        print('The mouse is moved')
    elif event == cv2.EVENT_MOUSEWHEEL:
        print('The mouse wheel is moving!')
    
    if flags == cv2.EVENT_FLAG_CTRLKEY:
        print('The control key is being pressed')

def checkKeyEvent():
    key_code = cv2.waitKey(1)
    
    if key_code != -1: # this is for a bug on Linux
        key_code &= 0xFF
        print('Key pressed', key_code)
    
    return key_code

capture = cv2.VideoCapture(0)
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, onMouseEvent)


success, frame = capture.read()
key_code = cv2.waitKey(1)
while success and key_code == -1:
    cv2.imshow(window_name, frame)
    success, frame = capture.read()
    key_code = checkKeyEvent()


cv2.destroyWindow(window_name)
capture.release()