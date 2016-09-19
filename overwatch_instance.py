from PIL import ImageGrab
import numpy as np
import cv2
import win32api,win32con

class overwatch_instance:
    def __init__(self,bbox = None,enable_display = False,freq = 30):
        self.enable_display = enable_display
        self.freq = freq
        self.bbox = bbox
        self.hold_keep_time = 0
        self.infire = False
        self.realtime_frame = self.capture()

    def capture(self):
        img = ImageGrab.grab(self.bbox)
        img_np = np.array(img,dtype=np.uint8)
        self.realtime_frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        return self.realtime_frame
    def get_realtime_frame(self):
        return self.realtime_frame
    def set_mouse_movement(self,x,y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(x),int(y))
    def shot(self,keeptime = 0):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        if keeptime == 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        else:
            self.infire = True
            self.hold_keep_time = keeptime

    def release_shot(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        self.infire = False

    def main_thread(self):
        while True:
            self.capture()
            if self.enable_display:
                res = cv2.resize(self.get_realtime_frame(), None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
                cv2.imshow("overwatch_instance_debug",res)
            cv2.waitKey(1000/self.freq)

            if self.infire:
                self.hold_keep_time -= 1000/self.freq
                if self.hold_keep_time <= 0:
                    self.release_shot()



if __name__ == "__main__":
    overwatch_instance((0,0,1920,1200),True,30).main_thread()
