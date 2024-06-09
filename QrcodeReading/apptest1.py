from PyQt5.QtWidgets import QApplication
from PyQt5 import uic 
from callmain import MAIN
from qrcodereading1 import QRCodeReaderApp 

class UI():
    def __init__(self):
        super().__init__()
        self.main = MAIN()
        self.qrcode = QRCodeReaderApp()
        
if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    app.exec_()
        
        