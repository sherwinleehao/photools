import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        x = 0
        y = 0

        text = "x: %d,  y: %d !"%(x,y)
        self.msg = QLabel(text, self)
        self.setMouseTracking(True)

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
        self.setStyleSheet('#frame1{background-color:rgb(0,255,0)}'
                           '#frame1:hover{background-color:rgb(0,255,235)}')


        self.setGeometry(300, 200, 1000, 500)
        self.show()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        # print(x,y)
        text = "x: %d,y:%d      !"%(x,y)
        self.msg.setText(text)

    def mousePressEvent (self,  e):
        print("XXXXXXXXXXXXXX")

    def wheelEvent (self,  e):
        # print("WWWWWWWWWWWWWWWWWW")
        angle = e.angleDelta() / 8

        angleX = angle.x()
        angleY = angle.y()
        # print(angle.y())
        # print(e.x(),e.y())
        rawx = self.msg.pos().x()
        self.msg.move(angle.y()+rawx,0)

    def resizeEvent(self,e):
        print("Resize!")
        print(self.size())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())