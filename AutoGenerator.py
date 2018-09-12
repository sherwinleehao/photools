#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee
Website: Sherwinleehao.com
Last edited: 20180912

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
import cv2

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

        padding = ExportPanel.padding


        self.settingPanel = QLabel('', self)
        self.settingPanel.setObjectName("settingPanel")
        self.settingPanel.setStyleSheet('background-color:rgba(255,0,0,220);')
        self.settingPanel.setGeometry(padding, padding*2, self.width()-2*padding, self.height()-padding*5)
        self.settingPanelTitle = QLabel('Setting', self)
        self.settingPanelTitle.setObjectName("settingPanel_title")
        self.settingPanelTitle.setStyleSheet('background-color:rgba(0,255,0,220);')
        self.settingPanelTitle.setParent(self.settingPanel)
        self.settingPanelTitle.setFixedWidth(self.settingPanel.width())
        self.settingPanelTitle.setFixedHeight(padding)
        self.settingPanelTitle.setAlignment(Qt.AlignCenter)
        self.sphl = QHBoxLayout()

        productCount = 4
        productSize = 48
        gap = (self.settingPanel.width()-2*padding-productCount*productSize)/(productCount-1)

        self.product0 = QPushButton("0")
        self.product0.setParent(self.settingPanel)
        self.product0.setGeometry(padding+0*(productSize+gap),padding,productSize,productSize)
        self.product1 = QPushButton("1")
        self.product1.setParent(self.settingPanel)
        self.product1.setGeometry(padding+1*(productSize+gap), padding, productSize, productSize)
        self.product2 = QPushButton("2")
        self.product2.setParent(self.settingPanel)
        self.product2.setGeometry(padding+2*(productSize+gap), padding, productSize, productSize)
        self.product3 = QPushButton("3")
        self.product3.setParent(self.settingPanel)
        self.product3.setGeometry(padding+3*(productSize+gap), padding, productSize, productSize)

        self.exportProjectPathLabel = QLabel("Export Project Path:")
        self.exportProjectPathLabel.setParent(self.settingPanel)
        self.exportProjectPathLabel.setGeometry(padding, productSize+2*padding, (self.settingPanel.width()/2)-padding, 20)
        self.exportProjectPathLabel.setStyleSheet('background-color:rgb(0,0,255);')





        self.show()
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

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
        self.icon.setCursor(Qt.PointingHandCursor)

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
    musicPath = 'rawPath'
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
        self.icon.setCursor(Qt.PointingHandCursor)
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

        self.waveform = QLabel()
        self.waveform.setObjectName("MusicPanel_waveform")
        self.waveform.setParent(self.content)
        self.waveform.setGeometry(importBox_padding,0,self.w-2*importBox_padding, 80)
        self.waveform.setStyleSheet('image:url(./GUI/music-loading.png)')
        # self.waveform.setMask(QRegion(0,0,self.w-2*importBox_padding,80,QRegion.Ellipse))
        # self.waveform.setMask(QPixmap("GUI/music-mask.png").scaledToWidth(self.w-2*importBox_padding).mask())
        self.waveform.setVisible(False)


        # self.waveform.setStyleSheet('background-image:url(./GUI/music-loading.png)')
        # self.IMG = cv2.imread('´´GUI/music-loading.png')
        # pixmap = self.getResizeQpixmap(self.IMG,self.w-2*importBox_padding, 80)
        # self.waveform.setPixmap(pixmap)
        print('waveform:',self.w, self.h)
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())
        self.icon.clicked.connect(self.importMusic)

    def importMusic(self):
        file = self.openFileNamesDialog()[0]
        try:
            if '.mp3' not in file:
                QMessageBox.about(self, 'Not Supported Format','This Version We Just Support .MP3 files, Please Check.')
            else:
                MusicPanel.musicPath = file
                ##Here need to fix if the file is not only one will crash
        except:
            pass

        if MusicPanel.musicPath is not "rawPath":
            musicName = os.path.basename(MusicPanel.musicPath)
            self.waveform.setVisible(True)
            self.title.setText(musicName)
            self.waveform.setStyleSheet('image:url(./GUI/music-loading.png)')
            print('Start BackendLoadWaveformThread')
            self.backend = BackendLoadWaveformThread()
            self.backend.update_date.connect(self.updateWaveform)
            self.backend.start()


    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Please Select Your Footages", "",
                                                "All Files (*);;Media Files (*.mp3,*.wav,*.m4a)", options=options)
        if files:
            return files

    def getResizeQpixmap(self, IMG,width,height):
        st = time.time()
        img_h, img_w, _ = IMG.shape
        IMG = cv2.resize(IMG, None, fx=(height/img_h), fy=(width/img_w), interpolation=cv2.INTER_CUBIC)
        et = time.time()
        print("Resize Time:",et-st)
        cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB, IMG)
        img_h, img_w, bytesPerComponent = IMG.shape
        bytesPerLine = bytesPerComponent * img_w
        qmap = QImage(IMG.data, img_w, img_h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qmap)
        return pixmap

    def updateWaveform(self,waveformPath):
        print(waveformPath)
        self.waveform.setStyleSheet('image:url(%s)'%waveformPath)
        pass

    def removeWaveform(self):
        self.title.setText("Background Music")
        MusicPanel.musicPath = 'rawPath'
        self.waveform.setVisible(False)

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        changeAct = cmenu.addAction("Change Music")
        removeAct = cmenu.addAction("Remove Music")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        cmenu.setStyleSheet('background-color:rgb(148,61,71);')
        if action == changeAct:
            self.importMusic()
        elif action == removeAct:
            self.removeWaveform()
        elif action == quitAct:
            qApp.quit()

class ExportPanel(QWidget):
    w = 0
    h = 80
    label_h = 32
    padding = 0

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

        ExportPanel.padding = (self.h-self.label_h)/2
        self.export = QPushButton("      Export", self)
        self.export.setObjectName("ExportPanel_Export")
        self.export.setParent(self.content)
        self.export.setGeometry(ExportPanel.padding,ExportPanel.padding,(self.w-self.h),self.label_h)
        self.export.clicked.connect(self.exportData)
        self.export.setCursor(Qt.PointingHandCursor)

        self.setting = QPushButton("", self)
        self.setting.setObjectName("ExportPanel_Setting")
        self.setting.setParent(self.content)
        self.setting.setGeometry((self.w-self.h/2-self.label_h/2), (self.h - self.label_h) / 2,self.label_h,self.label_h)
        self.setting.setCursor(Qt.PointingHandCursor)



        self.layout.addWidget(self.content)
        self.setLayout(self.layout)
        self.start = QPoint(0, 0)
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())

    def exportData(self):
        print("This is Export!")
        print(MusicPanel.musicPath)
        print()



class BackendLoadWaveformThread(QThread):
    print('Backend Load Waveform Thread')
    update_date = pyqtSignal(str)
    def run(self):
        st = time.time()
        print(MusicPanel.musicPath)
        waveformPath = pt.findWaveform(MusicPanel.musicPath)
        self.update_date.emit(waveformPath)
        et = time.time()
        print("Use Time to Load Waveform: %.4f\n"%(et-st))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    if hasattr(QStyleFactory, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    mw = MainWindow()
    sys.exit(app.exec_())
