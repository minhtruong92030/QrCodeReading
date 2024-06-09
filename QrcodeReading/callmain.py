from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic 
from qrcodereading1 import QRCodeReaderApp
import sys

class MAIN(QMainWindow):
    def __init__(self):  
        super().__init__()
        uic.loadUi("qrcodeapp1.ui",self)
        self.qrcode = QRCodeReaderApp()
        self.qrcode.a_changed.connect(self.update_coca)
        self.qrcode.b_changed.connect(self.update_pepsi)
        self.show()
        self.qrcode.run()
    
    def update_coca(self, value):
        self.RegValueCoca.setText(str(value))
        # print("a = " + str(value))

    def update_pepsi(self,value):
        self.RegValuePepsi.setText(str(value))
        # print("b = " + str(value))

if __name__ == "__main__":
    app = QApplication([])
    ui = MAIN()
    app.exec_()
    
    
