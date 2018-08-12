import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np
import time
from photools import *

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.IMGPath = "img\\04.jpg"
        self.IMGPaths = getAllImgs('img')
        self.IMG = cv2.imread(self.IMGPath)

        self.setGeometry(300, 200, 1024, 500)
        self.canvas = QLabel("Hello world", self)
        pixmap = self.getResizeQpixmap(self.IMG)
        self.canvas.setPixmap(pixmap)
        self.canvas.resize(self.width(), self.height())
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setObjectName("canvas")

        pageUpButton = QPushButton()
        pageDownButton = QPushButton()
        TestButton = QPushButton()
        pageUpButton.setObjectName("pageUpButton")
        pageDownButton.setObjectName("pageDownButton")
        TestButton.setObjectName("TestButton")
        pageUpButton.clicked.connect(self.previous_Img)
        pageDownButton.clicked.connect(self.next_Img)
        TestButton.clicked.connect(self.TestFuntion)

        hbox = QHBoxLayout()
        hbox.addWidget(pageUpButton)
        hbox.addStretch(1)
        hbox.addWidget(TestButton)
        hbox.addStretch(1)
        hbox.addWidget(pageDownButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

        with open('style.qss', "r") as qss:
            self.setStyleSheet(qss.read())

        self.setWindowTitle('Photools')
        self.setMinimumSize(640, 480)
        self.show()

    def getResizeQpixmap(self, IMG):
        st = time.time()
        win_w = self.size().width()
        win_h = self.size().height()
        win_a = win_w / win_h
        img_h, img_w, _ = IMG.shape
        img_a = img_w / img_h
        if win_a > img_a:
            scale = win_h / img_h
        else:
            scale = win_w / img_w
        IMG = cv2.resize(IMG, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
        et = time.time()
        # print("Use :",et-st)
        # r = [0,0,win_w,win_h]
        # r = [12,12,500,500]

        # IMG_crop = IMG[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        # IMG_crop = IMG[0:500,0:500]
        # IMG_crop = cv2.resize(IMG_crop, None, fx=1.25, fy=1.25, interpolation=cv2.INTER_CUBIC)
        cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB, IMG)
        img_h, img_w, bytesPerComponent = IMG.shape
        bytesPerLine = bytesPerComponent * img_w
        qmap = QImage(IMG.data, img_w, img_h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qmap)
        return pixmap

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()

    # def wheelEvent(self, e):
    #     angle = e.angleDelta() / 8
    #     angleX = angle.x()
    #     angleY = angle.y()
    #     rawx = self.canvas.pos().x()
    #     self.canvas.move(angle.y() + rawx, 0)

    def resizeEvent(self, e):
        # print("Resize!")
        # print(self.size())
        win_w = self.size().width()
        win_h = self.size().height()
        self.canvas.setGeometry(0, 0, win_w, win_h)
        pixmap = self.getResizeQpixmap(self.IMG)
        self.canvas.setPixmap(pixmap)

    def next_Img(self):
        self.change_Img(1)

    def previous_Img(self):
        self.change_Img(-1)

    def TestFuntion(self, e):
        print("XXXXXXXX")
        pass
        print(self.IMGPath)

    def change_Img(self,deltaID):
        IMGIndex = self.IMGPaths.index(self.IMGPath)
        tempID = IMGIndex +deltaID
        if tempID >=len(self.IMGPaths):
            tempID = tempID-len(self.IMGPaths)
        elif tempID <0 :
            tempID = tempID+len(self.IMGPaths)
        print(tempID)
        self.IMGPath = self.IMGPaths[tempID]
        self.IMG = cv2.imread(self.IMGPath)
        pixmap = self.getResizeQpixmap(self.IMG)
        self.canvas.setPixmap(pixmap)
        print(self.IMGPath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
