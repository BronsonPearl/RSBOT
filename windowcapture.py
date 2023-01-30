import numpy as np
import win32gui
import win32ui
import win32con
from threading import Thread, Lock


class WindowCapture:
    
    #threading properites 
    stopped = True
    lock = None
    screenshot = None


    #properties
    w = 0
    h = 0
    hwnd = None
    titlebar = 32
    border = 10
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, window_name):
        #thread lock object
        self.lock = Lock()

        #find game window
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        #measuring for window border to capture only the game
        window_size = win32gui.GetWindowRect(self.hwnd)
        self.w = window_size[2] - window_size[0]
        self.h = window_size[3] - window_size[1]
        self.w = self.w - (self.border * 2)
        self.h = self.h - self.titlebar - self.border
        self.cropped_x = self.border
        self.cropped_y = self.titlebar

        #set cropped coords to translate to game screenshot
        self.offset_x = window_size[0] + self.cropped_x
        self.offset_y = window_size[1] + self.cropped_y
        
        


    def get_window(self):   
        #capture screen
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        #save bitmap and re-size
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        image = np.fromstring(signedIntsArray, dtype = 'uint8')
        image.shape = (self.h, self.w, 4)
        #release resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        #drop alpha channel to image
        image = image[:, :, :3]
        image = np.ascontiguousarray(image)

        return image


    #try to prevent errors if the game client window is moved
    def get_screen_position(self, position):
        return (position[0] + self.offset_x, position[1] + self.offset_y)

    def run(self):
        while not self.stopped:
            #get upadated game image
            screenshot = self.get_window()
            #lock thread
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()

    def start(self):
        self.stopped = False
        window_capture_thread = Thread(target=self.run)
        window_capture_thread.start()
    
    def stop(self):
        self.stopped = True