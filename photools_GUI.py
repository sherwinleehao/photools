#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee
Website: Sherwinleehao.com
Last edited: 20180813
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np
import time
import sip
from photools import *


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.IMGPath = "img/thumb/thumb_0006.jpg"
        self.IMGPaths = getAllImgs('img/thumb/')


        self.IMG = cv2.imread(self.IMGPath)


        self.setGeometry(300, 200, 1024, 500)
        self.canvas = QLabel("Hello world", self)
        pixmap = self.getResizeQpixmap(self.IMG)
        self.canvas.setPixmap(pixmap)
        self.canvas.resize(self.width(), self.height())
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setObjectName("canvas")

        self.thumbContainer = QLabel("", self)
        self.thumbContainer.setObjectName("thumbContainer")
        self.tchbox = QHBoxLayout()
        self.thumbContainer.setLayout(self.tchbox)




        pageUpButton = QPushButton()
        pageDownButton = QPushButton()
        pageUpButton.setObjectName("pageUpButton")
        pageDownButton.setObjectName("pageDownButton")
        pageUpButton.clicked.connect(self.previous_Img)
        pageDownButton.clicked.connect(self.next_Img)

        TestButton = QPushButton()
        TestButton.setObjectName("TestButton")
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

        self.mouseOldPosX = 0
        self.mouseOldPosY = 0
        self.mouseDown = 0
        self.thumbCount = int(0)

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

    # def contextMenuEvent(self, event):
    #     cmenu = QMenu(self)
    #     newAct = cmenu.addAction("New")
    #     opnAct = cmenu.addAction("Open")
    #     quitAct = cmenu.addAction("Quit")
    #     action = cmenu.exec_(self.mapToGlobal(event.pos()))
    #     if action == quitAct:
    #         qApp.quit()

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
        self.moveThumbContainer(win_w,win_h)
        self.createThumbs()

    def next_Img(self):
        self.change_Img(1)

    def previous_Img(self):
        self.change_Img(-1)

    def TestFuntion(self, e):
        print("XXXXXXXX")
        pass
        print(self.IMGPath)

    def change_Img(self, deltaID):
        IMGIndex = self.IMGPaths.index(self.IMGPath)
        tempID = IMGIndex + deltaID
        if tempID >= len(self.IMGPaths):
            tempID = tempID - len(self.IMGPaths)
        elif tempID < 0:
            tempID = tempID + len(self.IMGPaths)
        self.IMGPath = self.IMGPaths[tempID]
        self.IMG = cv2.imread(self.IMGPath)
        pixmap = self.getResizeQpixmap(self.IMG)
        self.canvas.setPixmap(pixmap)

    def mousePressEvent(self, e):
        self.mouseOldPosX = e.globalX()
        self.mouseOldPosY = e.globalY()
        self.mouseDown = e.button()

    def mouseReleaseEvent(self, e):
        self.mouseDown = 0

    def mouseMoveEvent(self, e):
        self.moveWindow(e)

    def moveWindow(self,e):
        if self.mouseDown == 1:
            x = e.globalX()
            y = e.globalY()
            deltaX = x - self.mouseOldPosX
            deltaY = y - self.mouseOldPosY
            self.mouseOldPosX = e.globalX()
            self.mouseOldPosY = e.globalY()
            self.move(deltaX+self.pos().x(),deltaY+self.pos().y())

    def moveThumbContainer(self,win_w,win_h):
        width = win_w*0.8
        height= 80
        maxThumbCount = width // height
        if len(self.IMGPaths) < maxThumbCount:
            maxThumbCount = len(self.IMGPaths)
        if maxThumbCount%2 ==0:
            maxThumbCount -= 1
        print("maxThumbCount :", maxThumbCount)
        width = maxThumbCount *85
        posX = int((win_w-width)*0.5)
        posY = win_h-height-10
        self.thumbCount = int(maxThumbCount)
        self.thumbContainer.setGeometry(posX,posY,width,height)


    def createThumbs(self):
        self.clearLayoutItems(self.tchbox)
        print("Count of widgets:", self.tchbox.count())

        for i in range(self.thumbCount):
            ThumbnailButton = QPushButton(str(i))
            ThumbnailButton.setObjectName("ThumbnailButton")
            self.tchbox.addStretch(1)
            self.tchbox.addWidget(ThumbnailButton)
        pass
        self.tchbox.addStretch(1)
        print("Count of widgets:", self.tchbox.count())

    def clearLayoutItems(self,layout):
        print("Clear Layout :",layout)
        while layout.count() >0:
            item = layout.takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.deleteLater()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
