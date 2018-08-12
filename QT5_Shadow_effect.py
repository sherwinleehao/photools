import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextBrowser, QWidget, QFrame,QGraphicsDropShadowEffect
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        TextBr = QTextBrowser(self)
        TextBr.setGeometry(400, 300, 300, 100)
        TextBr.setText('Test')

        rbtn = QPushButton('Red', self)
        rbtn.setObjectName("Red")
        rbtn.setGeometry(10,30,50,50)

        gbtn = QPushButton('Green', self)
        gbtn.setObjectName("Green")
        gbtn.setGeometry(10, 90, 50, 50)

        bbtn = QPushButton('Blue', self)
        bbtn.setObjectName("Blue")
        bbtn.setGeometry(10, 160, 50, 50)



        frm = QFrame(self)
        frm.setGeometry(200, 50, 500, 500)
        frm.setObjectName("frame1")
        frm2 = QFrame(self)
        frm2.setGeometry(250, 100, 100, 100)
        frm2.setObjectName("frame2")


        self.setGeometry(300, 200, 1000, 500)
        self.setWindowTitle('QSS learning')
        # self.setStyleSheet('QPushButton{background-color:rgb(0,255,0)}')
        self.setStyleSheet('#frame1{background-color:rgb(0,255,0)}'
                           '#frame1:hover{background-color:rgb(0,255,235)}'
                           '#frame2{background-color:rgb(0,255,0);border-radius:15px;}'
                           '#Red{background-color:rgb(128,0,0);border-radius:5px;}'
                           '#Red:hover{background-color:rgb(255,125,125);border-radius:25px;}'
                           '#Red:pressed {background-color:rgb(255,125,125)}')
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(2)
        self.shadow.setYOffset(5)
        self.shadow.setColor(QColor(0, 0, 0, 255))

        frm2.setGraphicsEffect(self.shadow)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())