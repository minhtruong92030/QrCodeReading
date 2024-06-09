import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request
from PyQt5.QtCore import pyqtSignal, QObject

#this is a script for QR code detected

# Camera IP's url
url = 'http://192.168.124.57/cam-hi.jpg'
font = cv2.FONT_HERSHEY_PLAIN

class QRCodeReaderApp(QObject):
    a_changed = pyqtSignal(int)
    b_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()  
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

        # If there's no QRcode detected
        if not decodedObjects:
            self.n =  self.n + 1
            #take 10 frames
            if( self.n >= 10):
                self.c = 0
            print(str(self.n))
        else:
            self.n = 0
        
        # Store regconized QRcode data
        for obj in decodedObjects:
            self.pres = obj.data
            if(self.c == 0):
                if self.pres.decode() == 'COCA':
                    self.a += 1
                    self.a_changed.emit(self.a)
                    self.c = 1

                    
                if self.pres.decode() == 'PEPSI':
                    self.b += 1
                    self.b_changed.emit(self.b)
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