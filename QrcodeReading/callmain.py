from PyQt5.QtWidgets import QMainWindow, QApplication
from qrcodereading1 import QRCodeReaderApp
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import cv2
import numpy as np
from qrcodepost import POST_sysrun
import sys

class MAIN(QMainWindow):

    def __init__(self):  
        super().__init__()
        uic.loadUi("qrcodeapp1.ui",self)
        self.qrcode0 = QRCodeReaderApp()
        self.count_running = True
        self.count_stopping = False
        #with this function, you should check callmain and qrcodereading1
        self.qrcode0.a_changed.connect(self.update_coca)
        self.qrcode0.b_changed.connect(self.update_pepsi)
        self.qrcode0.c_changed.connect(self.update_fanta)
        self.qrcode0.s_changed.connect(self.update_sum)
        self.qrcode0.data_changed.connect(self.update_data)
        self.StartButton.clicked.connect(self.send_start)
        self.StopButton.clicked.connect(self.send_stop)

        # this is buttons for camera display
        self.OnCamButton.clicked.connect(self.start_capture_video)
        self.OffCamButton.clicked.connect(self.stop_capture_video)

        self.thread = {}
        self.show()
        self.qrcode0.run()
    
    #this is for camera display
    def closeEvent(self, event):
        self.stop_capture_video()
    
    def stop_capture_video(self):
        if 1 in self.thread:
            self.thread[1].stop()
    
    def start_capture_video(self):
        self.thread[1] = capture_video(index = 1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_camera) #camera data runs in this thread by signal

    def show_camera(self, cv_img):
        """Cập nhật label với hình ảnh từ opencv"""
        qt_img = self.convert_cv_qt(cv_img)
        self.CameraDisplay.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Chuyển đổi từ hình ảnh opencv sang QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    #this is for updating quantities counted
    def update_data(self, data):
        self.DetectedData.setText(str(data))

    def update_coca(self, value):
        self.RegValueCoca.setText(str(value))

    def update_pepsi(self,value):
        self.RegValuePepsi.setText(str(value))

    def update_fanta(self,value):
        self.RegValueFanta.setText(str(value))

    def update_sum(self,value):
        self.RegValueSum.setText(str(value))

    def send_start(self):
        start ={
            'name' : 'START'
        }
        POST_sysrun(start)

    def send_stop(self):
        stop = {
            'name': 'STOP'
        }
        POST_sysrun(stop)

class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)
    
    def __init__(self, index):
        self.index = index
        self.qrcode = QRCodeReaderApp()
        super(capture_video, self).__init__()

    def run(self):
        while self.qrcode.running:
            cameraframe = self.qrcode.update_cameraframe()
            if cameraframe is not None:
                self.signal.emit(cameraframe)

    def stop(self):
        self.qrcode.running = False
        self.quit()
        self.wait()

if __name__ == "__main__":
    app = QApplication([])
    ui = MAIN()
    app.exec_()
    
    
