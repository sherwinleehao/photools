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
        # self.setMinimumSize(360, 720)
        self.setFixedSize(360,720)

        self.layout = QVBoxLayout()
        self.layout.addWidget(TitleBar(self))
        self.layout.addWidget(FootagesPanel(self))
        self.layout.addWidget(MusicPanel(self))
        self.layout.addWidget(ExportPanel(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addStretch(1)


        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.show()


class TitleBar(QWidget):
    logo_w = 120
    logo_h = 30
    w = 0
    h = 50
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        self.w = self.parent.width()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("123")
        self.title.setObjectName("TitleBar_title")

        self.logo = QLabel("")
        self.logo.setObjectName("TitleBar_logo")
        self.logo.setParent(self.title)
        offset_x = (self.w - self.logo_w)/2
        offset_y = (self.h - self.logo_h)/2
        self.logo.setGeometry(offset_x,offset_y,self.logo_w,self.logo_h)

        btn_size = 16
        padding = 4
        self.btn_close = QPushButton()
        self.btn_close.setObjectName("TitleBar_btn_close")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setParent(self.title)
        self.btn_close.setGeometry((self.w-btn_size-padding), padding, btn_size, btn_size)

        self.title.setFixedHeight(self.h)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        # self.layout.addWidget(self.btn_close)

        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())


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
    w = 0
    h = 470
    label = "Footages"
    label_h = 30

    def __init__(self, parent):
        super(FootagesPanel, self).__init__()
        self.parent = parent
        self.w = self.parent.width()
        self.setBaseSize(self.w, self.h)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.title = QLabel(self.label)
        self.title.setFixedHeight(self.label_h)
        self.content = QLabel()
        self.content.setFixedHeight(self.h - self.label_h)

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
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())


class MusicPanel(QWidget):
    w = 0
    h = 120
    label = "Background Music"
    label_h = 30

    def __init__(self, parent):
        super(MusicPanel, self).__init__()
        self.parent = parent
        self.w = self.parent.width()
        self.setBaseSize(self.w, self.h)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.title = QLabel(self.label)
        self.title.setFixedHeight(self.label_h)
        self.content = QLabel()
        self.content.setFixedHeight(self.h - self.label_h)

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
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())


class ExportPanel(QWidget):
    w = 0
    h = 80
    label_h = 32

    def __init__(self, parent):
        super(ExportPanel, self).__init__()
        self.parent = parent
        self.w = self.parent.width()
        # self.setBaseSize(self.w, self.h)
        self.setFixedSize(self.w, self.h)

        # self.content= QLabel('123456789')
        # self.content.setFixedHeight(self.h)
        # self.content.setStyleSheet('background-color: green;')
        # self.content.setFixedSize(self.w, self.h)
        self.hLayout = QHBoxLayout()
        self.hLayout.setSpacing(0)
        #
        self.export = QPushButton("Export", self)
        self.export.setObjectName("Export")
        self.export.setFixedHeight(self.label_h)
        self.export.setFixedWidth(self.w-(self.h-self.label_h)-self.label_h)
        # self.export.setAlignment(Qt.AlignCenter)

        self.setting = QPushButton("", self)
        self.setting.setObjectName("Setting")
        self.setting.setFixedHeight(self.label_h)
        self.setting.setFixedWidth(self.label_h)
        # self.setting.setAlignment(Qt.AlignCenter)

        self.hLayout.addStretch(1)
        self.hLayout.addWidget(self.export)
        self.hLayout.addWidget(self.setting)
        self.hLayout.addStretch(1)
        self.vLayout = QVBoxLayout()
        self.vLayout.setSpacing(0)
        self.vLayout.addStretch(1)
        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addStretch(1)
        self.setLayout(self.vLayout)

        self.start = QPoint(0, 0)
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
