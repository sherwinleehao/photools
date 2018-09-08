#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee
Website: Sherwinleehao.com
Last edited: 20180908

Task:


# 加入Add More和Remove，Remove All的按钮
#     添加多个文件到列表
    删除选中的文件
    # 删除全部文件
    # 弹窗显示已经在列表内的item

# 加载资源应该先加载占位缩略图，然后开启线程进行后台加载缩略图并替换

# 显示两行信息，文件名\n分辨率，帧率，
# 图片仅显示分辨率

修改列表缩略图的列表样式，修改滑动栏的样式，列表样式
做加载过程的占位GIF，完成后显示真缩图，缩略图将以MD5形式命名并缓存
视频文件后台获取25张图，划过能动态显示视频

鼠标悬停的Item上有删除按键


点击设置按钮能切换到设置页面，
    包括：输出路径 分辨率 帧率 是否分析 识别间隔 人脸识别  模糊度识别  直方图识别  运动趋势识别 重设为默认值

设置页面会优先读取Temp文件夹下的Json文件，反序列化为设置
对设置的修改也会后台修改该Json文件

点击分析后进入生成模式
    列表名称及进度
    暂停 停止



"""

import sys
from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os, random, time
import uuid, shutil
import photools as pt


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(TitleBar(self))
        self.layout.addWidget(FootagesPanel(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addStretch(-1)
        self.setMinimumSize(360, 720)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.show()


class TitleBar(QWidget):
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        print(self.parent.width())
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("Filmora Auto Generator")

        btn_size = 24

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size, btn_size)
        self.btn_close.setStyleSheet("background-color: red;")

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        # self.layout.addWidget(self.btn_min)
        # self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            background-color: black;
            color: white;
        """)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(TitleBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()


class FootagesPanel(QWidget):
    def __init__(self, parent):
        super(FootagesPanel, self).__init__()
        self.parent = parent
        print(self.parent.width())
        self.setBaseSize(self.parent.width(),380)
        # self.setStyleSheet("""
        #             background-color: red;
        #             color: white;
        #         """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.title = QLabel("Footages")
        self.title.setFixedHeight(30)
        self.content = QLabel()
        self.content.setFixedHeight(350)

        # self.title.setFixedHeight(380)

        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.content)
        self.title.setStyleSheet("""
                    background-color: blue;
                    color: white;
                """)
        self.content.setStyleSheet("""
                    background-color: red;
                    color: white;
                """)
        self.setLayout(self.layout)
        self.start = QPoint(0, 0)
        print('FootagesPanel height:',self.height())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
