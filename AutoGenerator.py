#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee
Website: Sherwinleehao.com
Last edited: 20180910

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




拖拽素材进UI可以根据文件类型激活导入边框，松手瞬间打印路径
拖入音频的时候就后台开始解码，松手瞬间开始绘制。

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

        btn_size = 12
        padding = 6
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
    icon_w = 85
    icon_h =64

    def __init__(self, parent):
        super(FootagesPanel, self).__init__()
        self.parent = parent
        self.w = self.parent.width()
        self.setBaseSize(self.w, self.h)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.title = QLabel(self.label)
        self.title.setObjectName("FootagesPanel_title")
        self.title.setFixedHeight(self.label_h)
        self.content = QLabel()
        self.content.setFixedHeight(self.h - self.label_h)
        self.content.setObjectName("FootagesPanel_content")

        offset_y = 10
        self.icon = QLabel()
        self.icon.setObjectName("FootagesPanel_icon")
        self.icon.setParent(self.content)
        self.icon.setGeometry((self.w-self.icon_w)/2,((self.h - self.label_h)-self.icon_h)/2-offset_y,self.icon_w,self.icon_h)

        self.icon_info = QLabel("Drag and Drop to Import your Footages")
        self.icon_info.setObjectName("FootagesPanel_icon_info")
        self.icon_info.setParent(self.content)
        self.icon_info.setGeometry(0,((self.h - self.label_h)-self.icon_h)/2+self.icon_h+offset_y,self.w,30)
        self.icon_info.setAlignment(Qt.AlignCenter)

        importBox_padding = 20
        self.importBox = QLabel()
        self.importBox.setObjectName("FootagesPanel_importBox")
        self.importBox.setParent(self.content)
        self.importBox.setGeometry(importBox_padding,0,(self.w-2*importBox_padding),(self.h - self.label_h-importBox_padding))

        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.content)
        self.setLayout(self.layout)
        self.start = QPoint(0, 0)
        self.importBox.setVisible(False)
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())


class MusicPanel(QWidget):
    w = 0
    h = 120
    label = "Background Music"
    label_h = 30
    icon_w = 64
    icon_h = 64

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
        self.title.setObjectName("MusicPanel_title")
        self.content = QLabel()
        self.content.setFixedHeight(self.h - self.label_h)
        self.content.setObjectName("MusicPanel_content")

        self.icon = QPushButton()
        self.icon.setObjectName("MusicPanel_icon")
        self.icon.setParent(self.content)
        self.icon.setGeometry((self.w-self.icon_w)/2,((self.h - self.label_h)-self.icon_h)/2,self.icon_w,self.icon_h)
        print('self.h',self.h)
        print('self.h',self.h)

        importBox_padding = 20
        self.importBox = QLabel()
        self.importBox.setObjectName("MusicPanel_importBox")
        self.importBox.setParent(self.content)
        self.importBox.setGeometry(importBox_padding,importBox_padding/2,(self.w-2*importBox_padding),(self.h - self.label_h-importBox_padding))


        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.content)
        self.setLayout(self.layout)
        self.start = QPoint(0, 0)
        self.importBox.setVisible(False)
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())

        self.icon.clicked.connect(self.importMusic)

    def importMusic(self):
        print("hello world!")
        files = self.openFileNamesDialog()
        musicFile = files[0]
        print(files)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Please Select Your Footages", "",
                                                "All Files (*);;Media Files (*.mp3,*.wav,*.m4a)", options=options)
        if files:
            return files


class ExportPanel(QWidget):
    w = 0
    h = 80
    label_h = 32

    def __init__(self, parent):
        super(ExportPanel, self).__init__()
        self.parent = parent
        self.w = self.parent.width()
        self.setFixedSize(self.w, self.h)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.content = QLabel()
        self.content.setGeometry(0,0,self.w,self.h)
        self.content.setObjectName("ExportPanel_content")


        self.export = QPushButton("      Export", self)
        self.export.setObjectName("ExportPanel_Export")
        self.export.setParent(self.content)
        self.export.setGeometry((self.h-self.label_h)/2,(self.h-self.label_h)/2,(self.w-self.h),self.label_h)


        self.setting = QPushButton("", self)
        self.setting.setObjectName("ExportPanel_Setting")
        self.setting.setParent(self.content)
        self.setting.setGeometry((self.w-self.h/2-self.label_h/2), (self.h - self.label_h) / 2,self.label_h,self.label_h)

        self.layout.addWidget(self.content)
        self.setLayout(self.layout)
        self.start = QPoint(0, 0)
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    if hasattr(QStyleFactory, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    mw = MainWindow()
    sys.exit(app.exec_())
