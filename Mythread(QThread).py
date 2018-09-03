# #coding=utf-8
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# import time
#
# '''
# 信号传参类型
# pyqtSignal()                               #无参数信号
# pyqtSignal(int)                            # 一个参数(整数)的信号
# pyqtSignal([int],[str]                     # 一个参数(整数或者字符串)重载版本的信号
# pyqtSignal(int,str)                        #二个参数(整数,字符串)的信号
# pyqtSignal([int,int],[int,str])          #二个参数([整数,整数]或者[整数,字符串])重载版本
# '''
#
#
# class Mythread(QThread):
#     # 定义信号,定义参数为str类型
#     breakSignal = pyqtSignal(str,str)
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         # 下面的初始化方法都可以，有的python版本不支持
#         #  super(Mythread, self).__init__()
#
#     def run(self):
#         for i in range(2000000):
#             # 发出信号
#             print(12)
#             # a=[i,i+1]
#             a=i*2
#
#             self.breakSignal.emit(str(i),str(a))
#             # 让程序休眠
#             time.sleep(0.1)
#
#
# if __name__ == '__main__':
#     app = QApplication([])
#     dlg = QDialog()
#     dlg.resize(400, 300)
#     dlg.setWindowTitle("自定义按钮测试")
#     dlgLayout = QVBoxLayout()
#     dlgLayout.setContentsMargins(40, 40, 40, 40)
#     btn = QPushButton('测试按钮')
#     dlgLayout.addWidget(btn)
#     dlgLayout.addStretch(40)
#     dlg.setLayout(dlgLayout)
#     dlg.show()
#
#
#     def chuli(aaa,bbb):
#         # dlg.setWindowTitle(s)
#         # btn.setText(a+str(s[0]*10))
#         btn.setText(aaa+bbb)
#
#     # 创建线程
#     thread = Mythread()
#     # # 注册信号处理函数
#     thread.breakSignal.connect(chuli)
#     # # 启动线程
#     thread.start()
#     dlg.exec_()
#     app.exit()

import sys
from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os, random, time
import uuid,shutil
import photools as pt
from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit
import time
import sys

class BackendThread(QThread):
     # 通过类成员对象定义信号
    update_date = pyqtSignal(str)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
     # 处理业务逻辑
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit( str(currTime) )
            print(time.time())
            time.sleep(0.2)

class Window(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('PyQt 5界面实时更新例子')
        self.resize(400, 100)
        self.input = QLineEdit(self)
        self.input.resize(400, 100)
        self.initUI()

    def initUI(self):
        self.btn_tester = QPushButton("tester", self)
        self.btn_tester.clicked.connect(self.backThread)

    def backThread(self):
          # 创建线程
        self.backend = BackendThread()
          # 连接信号
        self.backend.update_date.connect(self.handleDisplay)
          # 开始线程
        self.backend.start()

    # 将当前时间输出到文本框
    def handleDisplay(self, data):
        print(data)
        # self.input.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
