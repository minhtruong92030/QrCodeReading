from PyQt5.QtWidgets import QApplication
from PyQt5 import uic 
from callmain import MAIN
from qrcodereading1 import QRCodeReaderApp 

class UI():
    def __init__(self):
        super().__init__()
        self.main = MAIN()
        self.qrcode = QRCodeReaderApp()
        self.main.show()
        self.qrcode.run()
    
    # def qrrun(self):
    #     self.qrcode.run()
    #     self.main.show()
        
if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    ui.qrrun()
    app.exec_()
        
        