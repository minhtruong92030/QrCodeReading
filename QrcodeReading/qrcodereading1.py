import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request
from PyQt5.QtCore import pyqtSignal, QObject
from qrcodepost import POST

#this is a script for QR code detected
# Camera IP's url
url = 'http://192.168.124.57/cam-hi.jpg'
font = cv2.FONT_HERSHEY_PLAIN

class QRCodeReaderApp(QObject):
    a_changed = pyqtSignal(int)
    b_changed = pyqtSignal(int)
    c_changed = pyqtSignal(int)
    s_changed = pyqtSignal(int)
    data_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()  
        self.prev = ""
        self.pres = ""
        self.obj = ""
        self.a = 0
        self.b = 0
        self.c = 0
        self.s = 0
        self.running = True
        self.camerarunning = True
        self.d = 0
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
                self.d = 0
            # print(str(self.n))
        else:
            self.n = 0
        
        # Store regconized QRcode data
        for obj in decodedObjects:
            self.pres = obj.data
            self.decoded_data = self.pres.decode()
            self.data_changed.emit(self.decoded_data)
            if(self.d == 0):
                if self.decoded_data == 'COCA':
                    self.a += 1
                    self.a_changed.emit(self.a)
                    product ={
                        'name' : self.decoded_data
                    }          
                    POST(product)        
                    self.d = 1

                    
                if self.decoded_data == 'PEPSI':
                    self.b += 1
                    self.b_changed.emit(self.b)
                    product ={
                        'name' : self.decoded_data
                    }
                    POST(product)
                    self.d = 1

                if self.decoded_data == 'FANTA':
                    self.c += 1
                    self.c_changed.emit(self.c)
                    product ={
                        'name' : self.decoded_data
                    }          
                    POST(product)        
                    self.d = 1
            
            self.s = self.a + self.b + self.c
            self.s_changed.emit(self.s)
                

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
    
    def update_cameraframe(self):
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        cameraframe = cv2.imdecode(imgnp, -1)
        decodedObjects = pyzbar.decode(cameraframe)
        for obj in decodedObjects:
            cv2.putText(cameraframe, obj.data.decode(), (70, 70), font, 2, (255, 0, 0), 3)
        return cameraframe
    
    def camerarun(self):
        while self.camerarunning:
            cameraframe = self.update_cameraframe()
            if cameraframe is None:
                self.camerarunning = False
                break
        cv2.destroyAllWindows()
    

if __name__ == "__main__":
    app = QRCodeReaderApp()
    app.run()