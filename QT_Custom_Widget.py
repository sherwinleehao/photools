#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee
Website: Sherwinleehao.com
Last edited: 20180815
"""


#
#
#


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
        self.info = QLabel("Hello world :)")
        self.ssld = SuperSlider()
        # self.c.updateBW[int].connect(self.wid.setValue)
        # sld.valueChanged[int].connect(self.changeValue)
        hbox = QHBoxLayout()
        hbox.addWidget(self.ssld)
        vbox = QVBoxLayout()
        vbox.addWidget(self.info)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(300, 200, 640, 150)
        self.setWindowTitle('Custom Widget')
        self.show()


class SuperSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)
        self.value = 75

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        # font = QFont("Serif", 7, QFont.Light)
        # qp.setFont(font)
        qp.setRenderHint(QPainter.Antialiasing, True)
        # brush = QBrush(Qt.SolidPattern)
        # brush.setStyle(Qt.BDiagPattern)
        # qp.setBrush(brush)
        qp.drawRect(250, 195, 90, 60)
        qp.drawRect(0, 0, 200, 20)
        qp.drawLine(0, 0, 200, 20)
        # rectangle(10.0, 20.0, 80.0, 60.0)
        # qp.drawEllipse(30)
        for i in range(100):
            qp.setPen(Qt.red)
            # qp.drawPoint(i,i)
            qp.drawLine(6*i, 0, 5*i, 20)



class SuperSlider2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)
        self.value = 75
        self.num = [75, 150, 225, 300, 375, 450, 525, 600, 675]

    def setValue(self, value):
        self.value = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        font = QFont("Serif", 7, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / 10.0))

        till = int(((w / 750.0) * self.value))
        full = int(((w / 750.0) * 700))

        if self.value >=700:
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till-full, h)
        else:
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, till, h)

        pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

        j = 0

        for i in range(step, 10*step, step):
            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            qp.drawText(i-fw/2, h/2, str(self.num[j]))
            j = j + 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
