from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic 
import sys

class MAIN(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("qrcodeapp1.ui",self)
        # self.show()

# if __name__ == "__main__":
#     app = QApplication([])
#     myui = MAIN()
#     app.exec_()