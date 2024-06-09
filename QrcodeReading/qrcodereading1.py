import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request
from PyQt5.QtCore import pyqtSignal, QObject
import time

# URL của Camera IP
url = 'http://192.168.124.57/cam-hi.jpg'
font = cv2.FONT_HERSHEY_PLAIN

class QRCodeReaderApp(QObject):
    a_changed = pyqtSignal(int)
    b_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()  # Gọi phương thức __init__ của lớp cha (QObject)
        self.prev = ""
        self.pres = ""
        self.obj = ""
        self.a = 0
        self.b = 0
        self.running = True
        self.c = 0
        self.n = 0

    def update_frame(self):
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgnp, -1)
        decodedObjects = pyzbar.decode(frame)
        print("decodedObjects is non-empty:", bool(decodedObjects))
        print(decodedObjects)
        if not decodedObjects:
            #time.sleep(1)
            self.n =  self.n + 1
            if( self.n >= 10):
                self.c = 0
            print("aaaaaaaaaaaaa")
        else:
            self.n = 0
        for obj in decodedObjects:
            print(decodedObjects)
            self.pres = obj.data
            # print(pres)
            #if self.prev != self.pres:
            #self.prev = self.pres   #gan gia tri hien tai cho gia tri cu (hoac ban dau)
            #print(self.prev)
            if(self.c == 0):
                if self.pres.decode() == 'COCA':
                    self.a += 1
                    self.a_changed.emit(self.a)
                    # time.sleep(0.1)
                    self.c = 1

                    
                if self.pres.decode() == 'PEPSI':
                    self.b += 1
                    self.b_changed.emit(self.b)
                    # time.sleep(0.1)
                    self.c = 1
        
            cv2.putText(frame, obj.data.decode(), (70, 70), font, 2, (255, 0, 0), 3)
            
        cv2.imshow("live transmission", frame)
        key = cv2.waitKey(1)
        if key == 27:
            return False
        return True

    def run(self):
        while self.running:
            if not self.update_frame():
                self.running = False
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QRCodeReaderApp()
    app.run()