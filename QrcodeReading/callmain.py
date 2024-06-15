from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic 
from qrcodereading1 import QRCodeReaderApp
from qrcodepost import POST_sysrun
import sys

class MAIN(QMainWindow):
    def __init__(self):  
        super().__init__()
        uic.loadUi("qrcodeapp1.ui",self)
        self.qrcode = QRCodeReaderApp()
        #with this function, you should check callmain and qrcodereading1
        self.qrcode.a_changed.connect(self.update_coca)
        self.qrcode.b_changed.connect(self.update_pepsi)
        self.qrcode.c_changed.connect(self.update_fanta)
        self.qrcode.s_changed.connect(self.update_sum)
        self.StartButton.clicked.connect(self.send_start)
        self.StopButton.clicked.connect(self.send_stop)
        self.show()
        self.qrcode.run()
    
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
        


if __name__ == "__main__":
    app = QApplication([])
    ui = MAIN()
    app.exec_()
    
    
