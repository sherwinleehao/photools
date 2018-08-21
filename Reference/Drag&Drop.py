#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee
Website: Sherwinleehao.com
Last edited: 20180820

Task:

1.Drag and Drop to import the files

2.load image in the background

"""









import sys
from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         text0 = QLabel("Title0",self)
#         text0.move(10,10)
#         self.setGeometry(100, 100, 640, 360)
#         self.setWindowTitle("Pre-Research")
#
#         self.show()
#
#     def mousePressEvent(self, QMouseEvent):
#         print('PPPPPPP')
#
#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.accept()
#             print('xxxxxxxxx')
#         else:
#             event.ignore()
#
#     def dropEvent(self, event):
#         for url in event.mimeData().urls():
#             path = url.toLocalFile().toLocal8Bit().data()
#             if os.path.isfile(path):
#                 print(path)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())



class Button(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):

        # if e.mimeData().hasFormat('text/plain'):
        if e.mimeData().hasUrls():
            e.accept()
            print('xxxx')
        else:
            e.ignore()

    def dropEvent(self, e):

        self.setText(e.mimeData().text())


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        edit = QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.move(30, 65)

        button = Button("Button", self)
        # button.move(100, 65)
        button.setGeometry(100, 65,400,40)

        self.setWindowTitle('Simple drag and drop')
        self.setGeometry(300, 300, 500, 150)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()