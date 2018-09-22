#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee
Website: Sherwinleehao.com
Last edited: 20180917

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
import json


class MainWindow(QWidget):
    padding = 24
    m_w = 360
    m_h = 720
    f_h = 470

    def __init__(self):
        super(MainWindow, self).__init__()
        self.settings = {}

        self.setFixedSize(360, 720)
        self.layout = QVBoxLayout()
        self.layout.addWidget(TitleBar(self))

        self.footagesPanel = FootagesPanel(self)
        self.layout.addWidget(self.footagesPanel)

        self.musicPanel = MusicPanel(self)
        self.layout.addWidget(self.musicPanel)

        self.exportPanel = ExportPanel(self)
        self.layout.addWidget(self.exportPanel)

        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addStretch(1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False

        self.listView = Example()
        self.listView.setParent(self.footagesPanel)
        self.listView.setVisible(False)

        self.settingPanel = SettingPanel(self)
        self.settingPanel.setParent(self)

        # self.settingPanel.setVisible(False)

        self.footagesPanel.icon.clicked.connect(self.importFootages)
        self.footagesPanel.icon.clicked.connect(self.listView.addmore)
        self.listView.btn_removeall.clicked.connect(self.removeAllFootages)

        self.exportPanel.setting.clicked.connect(self.toggleSettingPanel)
        self.exportPanel.export.clicked.connect(self.dosomething)
        self.settingPanel.analysisResetButton.clicked.connect(self.loadSettings)
        self.settingPanel.analysisSaveButton.clicked.connect(self.saveSettings)

        # self.setGeometry(1500, 250, self.m_w, self.m_h)
        self.setGeometry(-450, 850, self.m_w, self.m_h)
        self.loadSettings()

        self.show()
        self.settingPanel.initAnimation()  # 需要在显示完窗口瞬间初始化元件位置

        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

    def dosomething(self):
        self.settingPanel.animationIn()

    def toggleSettingPanel(self):
        if self.settingPanel.status:
            self.settingPanel.animationOut()
            # self.settingPanel.setVisible(False)
        else:
            self.settingPanel.animationIn()

    def loadSettings(self):
        path = 'Temp/Settings.json'
        self.settings = json.loads(open(path, 'r').read())

        self.settingPanel.product0.setChecked(self.settings['default']['product0'])
        self.settingPanel.product1.setChecked(self.settings['default']['product1'])
        self.settingPanel.product2.setChecked(self.settings['default']['product2'])
        self.settingPanel.product3.setChecked(self.settings['default']['product3'])
        self.settingPanel.product4.setChecked(self.settings['default']['product4'])
        self.settingPanel.exportProjectPath.setText(self.settings['default']['ExportProjectPath'])
        self.settingPanel.resolutionCombo.setCurrentIndex(self.settings['default']['Resolution'])
        self.settingPanel.frameRateCombo.setCurrentIndex(self.settings['default']['FrameRate'])
        self.settingPanel.analysisCheckbox.setChecked(self.settings['default']['Analysis'])
        self.settingPanel.analysisMultiCore.setChecked(self.settings['default']['MutiCore'])
        self.settingPanel.analysisSampleFrameCombo.setCurrentIndex(self.settings['default']['Sample'])
        self.settingPanel.analysisFaceDetect.setChecked(self.settings['default']['FaceDetect'])
        self.settingPanel.analysisBlurDetect.setChecked(self.settings['default']['BlurDetect'])
        self.settingPanel.analysisHistogramDetect.setChecked(self.settings['default']['HistogramDetect'])
        self.settingPanel.analysisMotionDetect.setChecked(self.settings['default']['MotionDetect'])
        self.settingPanel.analysisVoiceDetect.setChecked(self.settings['default']['VoiceDetect'])

    def saveSettings(self):
        path = 'Temp/Settings.json'
        self.settings['custom']['product0'] = self.settingPanel.product0.isChecked()
        self.settings['custom']['product1'] = self.settingPanel.product1.isChecked()
        self.settings['custom']['product2'] = self.settingPanel.product2.isChecked()
        self.settings['custom']['product3'] = self.settingPanel.product3.isChecked()
        self.settings['custom']['product4'] = self.settingPanel.product4.isChecked()
        self.settings['custom']['ExportProjectPath'] = self.settingPanel.exportProjectPath.text()
        self.settings['custom']['Resolution'] = self.settingPanel.resolutionCombo.currentIndex()
        self.settings['custom']['FrameRate'] = self.settingPanel.frameRateCombo.currentIndex()
        self.settings['custom']['Analysis'] = self.settingPanel.analysisCheckbox.isChecked()
        self.settings['custom']['MutiCore'] = self.settingPanel.analysisMultiCore.isChecked()
        self.settings['custom']['Sample'] = self.settingPanel.analysisSampleFrameCombo.currentIndex()
        self.settings['custom']['FaceDetect'] = self.settingPanel.analysisFaceDetect.isChecked()
        self.settings['custom']['BlurDetect'] = self.settingPanel.analysisBlurDetect.isChecked()
        self.settings['custom']['HistogramDetect'] = self.settingPanel.analysisHistogramDetect.isChecked()
        self.settings['custom']['MotionDetect'] = self.settingPanel.analysisMotionDetect.isChecked()
        self.settings['custom']['VoiceDetect'] = self.settingPanel.analysisVoiceDetect.isChecked()

        jsonStr = json.dumps(self.settings, sort_keys=True, indent=4, separators=(',', ': '))
        foo = open(path, 'w')
        foo.write(jsonStr)
        foo.close()
        self.toggleSettingPanel()

    def importFootages(self):
        self.listView.setVisible(True)
        pass

    def removeAllFootages(self):
        self.listView.setVisible(False)
        pass


class SettingPanel(QWidget):
    w = 0
    h = 0
    label = "Setting"
    label_h = 30
    padding = 0
    status = True

    def __init__(self, parent):
        super(SettingPanel, self).__init__()
        self.attributes = {}
        self.animMainObjectList = []
        self.animSubObjectList = []

        self.parent = parent
        self.w = self.parent.width()
        self.h = self.parent.height()
        padding = ExportPanel.padding
        self.setGeometry(padding, 2 * padding, self.w - 2 * padding, self.h - 5 * padding)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title = QLabel(self.label)
        self.title.setFixedHeight(self.label_h)
        self.title.setObjectName("SettingPanel_title")
        self.content = QLabel("")
        self.content.setFixedHeight(self.h - 5 * padding - self.label_h)
        self.content.setObjectName("SettingPanel_content")

        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.content)
        self.setLayout(self.layout)
        self.start = QPoint(0, 0)
        print(self.w - 2 * padding, self.h - 5 * padding)
        productCount = 4
        productSize = 48

        self.productLayout = QHBoxLayout()
        self.product0 = QCheckBox("")
        self.product1 = QCheckBox("")
        self.product2 = QCheckBox("")
        self.product3 = QCheckBox("")
        self.product4 = QCheckBox("")
        self.product0.setObjectName("SettingPanel_product0")
        self.product1.setObjectName("SettingPanel_product1")
        self.product2.setObjectName("SettingPanel_product2")
        self.product3.setObjectName("SettingPanel_product3")
        self.product4.setObjectName("SettingPanel_product4")

        self.product0.setFixedSize(productSize, productSize)
        self.product1.setFixedSize(productSize, productSize)
        self.product2.setFixedSize(productSize, productSize)
        self.product3.setFixedSize(productSize, productSize)
        self.product4.setFixedSize(productSize, productSize)
        self.productLayout.addWidget(self.product0)
        self.productLayout.addStretch(1)
        self.productLayout.addWidget(self.product1)
        self.productLayout.addStretch(1)
        self.productLayout.addWidget(self.product2)
        self.productLayout.addStretch(1)
        self.productLayout.addWidget(self.product3)
        self.productLayout.addStretch(1)
        self.productLayout.addWidget(self.product4)

        self.contentLayout = QVBoxLayout()
        self.content.setLayout(self.contentLayout)
        self.contentLayout.addLayout(self.productLayout)
        self.contentLayout.addStretch(1)

        self.exportProjectPathLabel = QLabel('Export Project Path:')
        self.exportProjectPathLabel.setObjectName("SettingPanel_exportProjectPathLabel")
        self.contentLayout.addWidget(self.exportProjectPathLabel)

        self.exportProjectPathLayout = QHBoxLayout()
        self.exportProjectPathButton = QPushButton("")
        self.exportProjectPathButton.setObjectName("SettingPanel_exportProjectPathButton")
        self.exportProjectPathButton.setFixedSize(self.label_h, self.label_h)
        self.exportProjectPath = QLineEdit('D:/Test/Export/Untitle.FMP', self)
        self.exportProjectPath.setObjectName("SettingPanel_exportProjectPath")
        self.exportProjectPath.setFixedHeight(self.label_h)
        self.exportProjectPath.setGeometry(0, 0, 250, 20)
        self.exportProjectPathLayout.addWidget(self.exportProjectPath)
        self.exportProjectPathLayout.addWidget(self.exportProjectPathButton)
        self.exportProjectPathLayout.setSpacing(0)
        self.contentLayout.addLayout(self.exportProjectPathLayout)
        self.contentLayout.addStretch(1)

        self.AttributesLayout = QHBoxLayout()

        self.resolutionLayout = QVBoxLayout()
        self.resolutionLayout.setSpacing(2)
        self.resolutionLabel = QLabel(" Resolution")
        self.resolutionLabel.setObjectName("SettingPanel_resolutionLabel")
        self.resolutionCombo = QComboBox(self)
        self.resolutionCombo.addItem("3840 x 2160")
        self.resolutionCombo.addItem("2560 x 1440")
        self.resolutionCombo.addItem("1920 x 1080")
        self.resolutionCombo.addItem("1280 x 720")
        self.resolutionCombo.addItem("960 x 540")
        self.resolutionLayout.addWidget(self.resolutionLabel)
        self.resolutionLayout.addWidget(self.resolutionCombo)

        self.frameRateLayout = QVBoxLayout()
        self.frameRateLayout.setSpacing(2)
        self.frameRateLabel = QLabel(" Frame Rate:")
        self.frameRateLabel.setObjectName("SettingPanel_frameRateLabel")
        self.frameRateCombo = QComboBox(self)
        self.frameRateCombo.addItem("60 FPS")
        self.frameRateCombo.addItem("50 FPS")
        self.frameRateCombo.addItem("30 FPS")
        self.frameRateCombo.addItem("25 FPS")
        self.frameRateCombo.addItem("24 FPS")
        self.frameRateLayout.addWidget(self.frameRateLabel)
        self.frameRateLayout.addWidget(self.frameRateCombo)

        self.AttributesLayout.addLayout(self.resolutionLayout)
        self.AttributesLayout.addLayout(self.frameRateLayout)
        self.AttributesLayout.setSpacing(20)
        self.contentLayout.addLayout(self.AttributesLayout)
        self.contentLayout.addStretch(1)

        self.analysisCheckbox = QCheckBox("Analysis", self)
        self.analysisCheckbox.setObjectName("SettingPanel_analysisCheckbox")
        self.contentLayout.addWidget(self.analysisCheckbox)
        self.analysisContent = QLabel("", self)
        self.analysisContent.setObjectName("SettingPanel_analysisContent")
        self.analysisContent.setFixedHeight(290)
        self.analysisContent.setFixedWidth(286)

        self.analysisLayout = QVBoxLayout()
        self.analysisContent.setLayout(self.analysisLayout)

        self.analysisLabel = QLabel(
            "In Order to get a better result\nAnalysis your footages will be necessary\nThese data can let us know more about your shot\nWhile needs more time.")
        self.analysisLabel.setObjectName("SettingPanel_analysisLabel")
        self.analysisLayout.addWidget(self.analysisLabel)

        self.analysisLayout.addStretch(1)

        self.analysisMultiCore = QCheckBox("Multi-Core Enhance", self)
        self.analysisLayout.addWidget(self.analysisMultiCore)

        self.analysisLayout.addStretch(1)

        self.analysisSampleFrameLayout = QHBoxLayout()
        self.analysisSampleFrameLabel = QLabel("Sample:")
        self.analysisSampleFrameLabel.setObjectName("SettingPanel_analysisSampleFrameLabel")
        self.analysisSampleFrameLabel.setFixedWidth(2.5 * padding)
        self.analysisSampleFrameCombo = QComboBox(self)
        self.analysisSampleFrameCombo.setObjectName("SettingPanel_analysisSampleFrameCombo")
        self.analysisSampleFrameCombo.addItem("Smart Sample")
        self.analysisSampleFrameCombo.addItem("Every Frame")
        self.analysisSampleFrameCombo.addItem("Every 2 Frame")
        self.analysisSampleFrameCombo.addItem("Every 5 Frame")
        self.analysisSampleFrameCombo.addItem("Every 10 Frame")
        self.analysisSampleFrameLayout.addWidget(self.analysisSampleFrameLabel)
        self.analysisSampleFrameLayout.addWidget(self.analysisSampleFrameCombo)
        self.analysisLayout.addLayout(self.analysisSampleFrameLayout)

        self.analysisLayout.addStretch(1)

        self.analysisFaceDetect = QCheckBox("Face Detect", self)
        self.analysisBlurDetect = QCheckBox("Blur Detect", self)
        self.analysisHistogramDetect = QCheckBox("Histogram Detect", self)
        self.analysisMotionDetect = QCheckBox("Motion Detect", self)
        self.analysisVoiceDetect = QCheckBox("Voice Detect", self)
        self.analysisLayout.addWidget(self.analysisFaceDetect)
        self.analysisLayout.addWidget(self.analysisBlurDetect)
        self.analysisLayout.addWidget(self.analysisHistogramDetect)
        self.analysisLayout.addWidget(self.analysisMotionDetect)
        self.analysisLayout.addWidget(self.analysisVoiceDetect)
        self.contentLayout.addWidget(self.analysisContent)

        self.contentLayout.addStretch(1)

        self.analysisSaveLayout = QHBoxLayout()
        self.analysisSaveLayout.setSpacing(0)
        self.analysisSaveButton = QPushButton("Save Settings", self)
        self.analysisSaveButton.setObjectName("SettingPanel_analysisSaveButton")
        self.analysisResetButton = QPushButton("", self)
        self.analysisResetButton.setObjectName("SettingPanel_analysisResetButton")
        self.analysisSaveButton.setFixedHeight(self.label_h)
        self.analysisResetButton.setFixedSize(self.label_h, self.label_h)
        self.analysisSaveLayout.addWidget(self.analysisSaveButton)
        self.analysisSaveLayout.addWidget(self.analysisResetButton)
        self.contentLayout.addLayout(self.analysisSaveLayout)

        self.contentLayout.addStretch(1)

        self.analysisCover = QLabel()
        self.analysisCover.setObjectName("SettingPanel_analysisCover")
        self.analysisCover.setParent(self.analysisContent)
        self.analysisCover.setFixedSize(self.analysisContent.width(), self.analysisContent.height())
        self.analysisCover.setVisible(False)

        self.analysisCheckbox.setChecked(True)
        self.analysisCheckbox.stateChanged.connect(self.togglenalysisCover)

        # self.initAnimation()
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())

    def initAnimation(self):
        print('initAnimation')
        group0 = []
        group0.append([0, self.title])
        group0.append([0, self.content])
        self.animSubObjectList.append(group0)

        group1 = []
        group1.append([1, self.product0])
        group1.append([1, self.product1])
        group1.append([1, self.product2])
        group1.append([1, self.product3])
        group1.append([1, self.product4])
        self.animSubObjectList.append(group1)

        group2 = []
        group2.append([2, self.exportProjectPathLabel])
        group2.append([2, self.exportProjectPath])
        group2.append([2, self.exportProjectPathButton])
        group2.append([2, self.resolutionLabel])
        group2.append([2, self.resolutionCombo])
        group2.append([2, self.frameRateLabel])
        group2.append([2, self.frameRateCombo])
        self.animSubObjectList.append(group2)

        group3 = []
        group3.append([3, self.analysisCheckbox])
        group3.append([3, self.analysisContent])
        group3.append([3, self.analysisLabel])
        group3.append([3, self.analysisMultiCore])
        group3.append([3, self.analysisSampleFrameLabel])
        group3.append([3, self.analysisSampleFrameCombo])
        group3.append([3, self.analysisFaceDetect])
        group3.append([3, self.analysisBlurDetect])
        group3.append([3, self.analysisHistogramDetect])
        group3.append([3, self.analysisMotionDetect])
        group3.append([3, self.analysisVoiceDetect])
        self.animSubObjectList.append(group3)

        group4 = []
        group4.append([4, self.analysisSaveButton])
        group4.append([4, self.analysisResetButton])
        self.animSubObjectList.append(group4)

        for group in self.animSubObjectList:
            for obj in group:
                obj.append(obj[1].pos())

        print(self.animSubObjectList)
        for x in self.animSubObjectList:
            print(x)

    def togglenalysisCover(self, state):
        if state == Qt.Checked:
            print('Checked')
            self.analysisCover.setVisible(False)
        else:
            print('UnChecked')
            self.analysisCover.setVisible(True)

    def resetSetting(self):
        pass

    def saveSetting(self):
        pass

    def animationIn(self):
        print("animationIn")
        self.status = True
        self.setVisible(True)
        self.group = QParallelAnimationGroup()
        Duration = 1000
        m_w = MainWindow.m_w
        groupID = 0
        for group in self.animSubObjectList:
            groupID += 1
            objID = 0
            for obj in group:
                objID += 1
                locals()['anim_' + str(groupID) + str(objID)] = QPropertyAnimation(obj[1], b"pos")
                locals()['anim_' + str(groupID) + str(objID)].setDuration(objID * Duration/len(group))
                locals()['anim_' + str(groupID) + str(objID)].setStartValue(QPointF(obj[2].x() + m_w, obj[2].y()))
                locals()['anim_' + str(groupID) + str(objID)].setEndValue(obj[2])
                # locals()['anim_' + str(groupID) + str(objID)].setEasingCurve(QEasingCurve.OutExpo)
                locals()['anim_' + str(groupID) + str(objID)].setEasingCurve(QEasingCurve.OutBack)

                if groupID == 1 :
                    locals()['anim_' + str(groupID) + str(objID)].setDuration(800)
                    locals()['anim_' + str(groupID) + str(objID)].setEasingCurve(QEasingCurve.OutExpo)
                elif groupID == 5 :
                    locals()['anim_' + str(groupID) + str(objID)].setDuration(500)

                self.group.addAnimation(locals()['anim_' + str(groupID) + str(objID)])

        self.group.start()

    def animationOut(self):
        print("animationOut")
        self.status = False
        self.group = QParallelAnimationGroup()
        Duration = 1000
        m_w = MainWindow.m_w
        groupID = 0
        for group in self.animSubObjectList:
            groupID += 1
            objID = 0
            for obj in group:
                objID += 1
                locals()['anim_' + str(groupID) + str(objID)] = QPropertyAnimation(obj[1], b"pos")
                locals()['anim_' + str(groupID) + str(objID)].setDuration(objID * Duration/len(group))
                locals()['anim_' + str(groupID) + str(objID)].setStartValue(obj[2])
                locals()['anim_' + str(groupID) + str(objID)].setEndValue(QPointF(obj[2].x() +m_w, obj[2].y()))
                locals()['anim_' + str(groupID) + str(objID)].setEasingCurve(QEasingCurve.InExpo)

                if groupID == 1 :
                    locals()['anim_' + str(groupID) + str(objID)].setDuration(500)
                    locals()['anim_' + str(groupID) + str(objID)].setEasingCurve(QEasingCurve.InExpo)
                elif groupID == 5 :
                    locals()['anim_' + str(groupID) + str(objID)].setDuration(500)

                self.group.addAnimation(locals()['anim_' + str(groupID) + str(objID)])
        self.group.start()
        self.group.finished.connect(self.disVisible)

    def disVisible(self):
        self.setVisible(False)


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
        offset_x = (self.w - self.logo_w) / 2
        offset_y = (self.h - self.logo_h) / 2
        self.logo.setGeometry(offset_x, offset_y, self.logo_w, self.logo_h)

        btn_size = 12
        padding = 6
        self.btn_close = QPushButton()
        self.btn_close.setObjectName("TitleBar_btn_close")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setParent(self.title)
        self.btn_close.setGeometry((self.w - btn_size - padding), padding, btn_size, btn_size)

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
    label = "Footages"
    label_h = 30
    icon_w = 85
    icon_h = 64

    def __init__(self, parent):
        super(FootagesPanel, self).__init__()
        self.parent = parent
        self.w = self.parent.width()
        self.h = MainWindow.f_h
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

        offset_y = 30
        self.icon = QPushButton()
        self.icon.setObjectName("FootagesPanel_icon")
        self.icon.setParent(self.content)
        self.icon.setGeometry((self.w - self.icon_w) / 2, ((self.h - self.label_h) - self.icon_h) / 2 - offset_y,
                              self.icon_w, self.icon_h)

        self.icon_info = QLabel("Drag and Drop to Import your Footages")
        self.icon_info.setObjectName("FootagesPanel_icon_info")
        self.icon_info.setParent(self.content)
        self.icon_info.setGeometry(0, ((self.h - self.label_h) - self.icon_h) / 2 + self.icon_h, self.w, 30)
        self.icon_info.setAlignment(Qt.AlignCenter)
        self.icon.setCursor(Qt.PointingHandCursor)

        importBox_padding = 20
        self.importBox = QLabel()
        self.importBox.setObjectName("FootagesPanel_importBox")
        self.importBox.setParent(self.content)
        self.importBox.setGeometry(importBox_padding, 0, (self.w - 2 * importBox_padding),
                                   (self.h - self.label_h - importBox_padding))

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
        self.icon.setGeometry((self.w - self.icon_w) / 2, ((self.h - self.label_h) - self.icon_h) / 2, self.icon_w,
                              self.icon_h)
        self.icon.setCursor(Qt.PointingHandCursor)
        importBox_padding = 20
        self.importBox = QLabel()
        self.importBox.setObjectName("MusicPanel_importBox")
        self.importBox.setParent(self.content)
        self.importBox.setGeometry(importBox_padding, importBox_padding / 2, (self.w - 2 * importBox_padding),
                                   (self.h - self.label_h - importBox_padding))

        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.content)
        self.setLayout(self.layout)
        self.start = QPoint(0, 0)
        self.importBox.setVisible(False)

        self.waveform = QLabel()
        self.waveform.setObjectName("MusicPanel_waveform")
        self.waveform.setParent(self.content)
        self.waveform.setGeometry(importBox_padding, 0, self.w - 2 * importBox_padding, 80)
        self.waveform.setStyleSheet('image:url(./GUI/music-loading.png)')
        # self.waveform.setMask(QRegion(0,0,self.w-2*importBox_padding,80,QRegion.Ellipse))
        # self.waveform.setMask(QPixmap("GUI/music-mask.png").scaledToWidth(self.w-2*importBox_padding).mask())
        self.waveform.setVisible(False)

        # self.waveform.setStyleSheet('background-image:url(./GUI/music-loading.png)')
        # self.IMG = cv2.imread('´´GUI/music-loading.png')
        # pixmap = self.getResizeQpixmap(self.IMG,self.w-2*importBox_padding, 80)
        # self.waveform.setPixmap(pixmap)
        print('waveform:', self.w, self.h)
        with open('APG.qss', "r") as qss:
            self.setStyleSheet(qss.read())
        self.icon.clicked.connect(self.importMusic)

    def importMusic(self):
        file = self.openFileNamesDialog()[0]
        try:
            if '.mp3' not in file:
                QMessageBox.about(self, 'Not Supported Format',
                                  'This Version We Just Support .MP3 files, Please Check.')
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

    def getResizeQpixmap(self, IMG, width, height):
        st = time.time()
        img_h, img_w, _ = IMG.shape
        IMG = cv2.resize(IMG, None, fx=(height / img_h), fy=(width / img_w), interpolation=cv2.INTER_CUBIC)
        et = time.time()
        print("Resize Time:", et - st)
        cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB, IMG)
        img_h, img_w, bytesPerComponent = IMG.shape
        bytesPerLine = bytesPerComponent * img_w
        qmap = QImage(IMG.data, img_w, img_h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qmap)
        return pixmap

    def updateWaveform(self, waveformPath):
        print(waveformPath)
        self.waveform.setStyleSheet('image:url(%s)' % waveformPath)
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
        self.content.setGeometry(0, 0, self.w, self.h)
        self.content.setObjectName("ExportPanel_content")

        ExportPanel.padding = (self.h - self.label_h) / 2
        self.export = QPushButton("      Export", self)
        self.export.setObjectName("ExportPanel_Export")
        self.export.setParent(self.content)
        self.export.setGeometry(ExportPanel.padding, ExportPanel.padding, (self.w - self.h), self.label_h)
        self.export.clicked.connect(self.exportData)
        self.export.setCursor(Qt.PointingHandCursor)

        self.setting = QPushButton("", self)
        self.setting.setObjectName("ExportPanel_Setting")
        self.setting.setParent(self.content)
        self.setting.setGeometry((self.w - self.h / 2 - self.label_h / 2), (self.h - self.label_h) / 2, self.label_h,
                                 self.label_h)

        # self.setting.clicked.connect(self.toggleSettingPanel)
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
        # def toggleSettingPanel(self):
        #     print('toggleSettingPanel')
        #     print('SettingPanel.isVisible()',self.SettingPanel.h)
        #     pass


class BackendLoadWaveformThread(QThread):
    print('Backend Load Waveform Thread')
    update_date = pyqtSignal(str)

    def run(self):
        st = time.time()
        print(MusicPanel.musicPath)
        waveformPath = pt.findWaveform(MusicPanel.musicPath)
        self.update_date.emit(waveformPath)
        et = time.time()
        print("Use Time to Load Waveform: %.4f\n" % (et - st))


class ListView(QListView):
    map_listview = []

    def __init__(self):
        super().__init__()
        self.m_pModel = ListModel()
        self.setModel(self.m_pModel)

    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除", pmenu)
            pDeleteAct.setShortcut('Del')
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            pmenu.addAction(pDeleteAct)
            pmenu.popup(self.mapToGlobal(event.pos()))

    def deleteItemSlot(self):
        index = self.currentIndex().row()
        print("deleteItemSlot ", index)
        if index > -1:
            self.m_pModel.deleteItem(index)

    def addItem(self, pitem):
        self.m_pModel.addItem(pitem)

    def removeItem(self, index):
        self.m_pModel.deleteItem(index)

    def showSelection(self):
        print(self.currentIndex().row())


class ListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.ListItemData = []
        self.Data_init()

    def data(self, index, role):
        # print("data:",index.isValid(),index.row,role)
        if index.isValid() or (0 <= index.row() < len(self.ListItemData)):
            if role == Qt.DisplayRole:
                # return QVariant(self.ListItemData[index.row()]['name'])
                return QVariant(self.parseItem(self.ListItemData[index.row()]))
            elif role == Qt.DecorationRole:
                return QVariant(QIcon(self.ListItemData[index.row()]['iconPath']))
            elif role == Qt.SizeHintRole:
                return QVariant(QSize(70, 80))
            elif role == Qt.TextAlignmentRole:
                # return QVariant(int(Qt.AlignHCenter | Qt.AlignVCenter))
                return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))
            elif role == Qt.FontRole:
                font = QFont()
                font.setPixelSize(12)
                return QVariant(font)
        else:
            return QVariant()

    def rowCount(self, parent=QModelIndex()):
        return len(self.ListItemData)

    def Data_init(self):
        print('Data_init')
        # randomnum = random.sample(range(100), 5)
        # for i in randomnum:
        #     randname = str("Sherwin %d" % i)
        #     ItemData = {'name': '', 'iconPath': ''}
        #     ItemData['name'] = randname
        #     ItemData['iconPath'] = "img/thumb/thumb_%04d.jpg" % i
        #     self.ListItemData.append(ItemData)
        #     print("ItemData", ItemData)

    def addItem(self, itemData):
        print('addItem')
        if itemData:
            self.beginInsertRows(QModelIndex(), len(self.ListItemData), len(self.ListItemData) + 1)
            self.ListItemData.append(itemData)
            self.endInsertRows()

    def deleteItem(self, index):
        print('deleteItem', index)
        del self.ListItemData[index]

    def getItem(self, index):
        print('getItem', index)
        if index > -1 and index < len(self.ListItemData):
            return self.ListItemData[index]

    def parseItem(self, item):
        name = item['name']
        # iconPath = item['iconPath']
        # filePath = item['filePath']
        mediaInfo = item['mediaInfo']
        tempStr = name + "\n" + mediaInfo
        print(tempStr)
        return tempStr


class Example(QWidget):
    updateList = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.bg = QLabel("", self)
        self.bg.setObjectName("ListView_BG")
        self.bg.setFixedSize(MainWindow.m_w, MainWindow.m_h)

        self.pListView = ListView()
        self.pListView.setViewMode(QListView.ListMode)
        # self.pListView.setViewMode(QListView.IconMode)
        self.pListView.setObjectName("ListView_pListView")
        self.pListView.setStyleSheet("QListView{icon-size:120px}")

        self.btn_addmore = QPushButton("Add More", self)
        self.btn_addmore.setObjectName("ListView_btn_addmore")
        self.btn_removeall = QPushButton("Remove All", self)
        self.btn_removeall.setObjectName("ListView_btn_removeall")
        self.btn_Mode = QPushButton("Mode", self)
        self.btn_Mode.setObjectName("ListView_btn_Mode")

        self.btn_addmore.setFixedSize(4 * MainWindow.padding, MainWindow.padding)
        self.btn_removeall.setFixedSize(4 * MainWindow.padding, MainWindow.padding)
        self.btn_Mode.setFixedSize(2 * MainWindow.padding, MainWindow.padding)

        Hbox = QHBoxLayout()
        Hbox.addWidget(self.btn_addmore)
        Hbox.addStretch(1)
        Hbox.addWidget(self.btn_Mode)
        Hbox.addWidget(self.btn_removeall)

        Vbox = QVBoxLayout()
        Vbox.addLayout(Hbox)
        Vbox.addWidget(self.pListView)

        self.setLayout(Vbox)

        Vbox.setContentsMargins(0, 0, 0, 0)
        Vbox.setSpacing(0)

        self.setGeometry(MainWindow.padding, 0, MainWindow.m_w - 2 * MainWindow.padding,
                         MainWindow.f_h - MainWindow.padding)
        self.btn_addmore.clicked.connect(self.addmore)
        self.btn_removeall.clicked.connect(self.removeall)
        self.btn_Mode.clicked.connect(self.toggleViewMode)

    def addmore(self):
        print("This is addmore!")
        filePaths = self.getfilePathList()
        print("Filepaths", filePaths)
        files = self.openFileNamesDialog()
        existFiles = []
        unsupportedFiles = []
        msg = ''
        if files:
            for file in files:
                basename = os.path.basename(file)
                name = basename.split(".")[0]
                ItemData = {}
                ItemData['name'] = name
                ItemKind = pt.getFileKind(file)
                ItemData['iconPath'] = "GUI/%sThumbnail.png" % ItemKind
                ItemData['filePath'] = file
                ItemData['mediaInfo'] = "Reselution FPS\nDuration"
                # if ItemKind is "video":
                #     mediaInfo = pt.getMediaInfo(file)
                #     print(mediaInfo)
                #     ItemData['mediaInfo']= mediaInfo

                if ItemData['filePath'] in filePaths:
                    print("\n", basename, "Already in the list!")
                    existFiles.append(basename)
                    pass
                elif ItemKind is None:
                    unsupportedFiles.append(basename)
                else:
                    self.pListView.addItem(ItemData)
                    self.updateList.append(file)
        if existFiles:
            tempmsg = str(existFiles).replace('[', '').replace(']', '').replace(',', '\n').replace(' ', '').replace(
                '\'', '')
            msg = msg + '\n' + tempmsg[:300] + "...\nAlready in the list.\n...\n"
        if unsupportedFiles:
            tempmsg = str(unsupportedFiles).replace('[', '').replace(']', '').replace(',', '\n').replace(' ',
                                                                                                         '').replace(
                '\'', '')
            msg = msg + '\n' + tempmsg[:300] + "...\nNot Supported.\n...\n"
        if msg:
            print(msg)
            QMessageBox.about(self, 'Files already in the list', msg)
        if self.updateList:
            self.backend = BackendThread()
            self.backend.update_date.connect(self.updateThumb)
            self.backend.start()
            pass

    def updateThumb(self, filePath, iconPath, mediaInfo):
        print(filePath)
        print(iconPath)
        print('\n')
        for i in self.pListView.m_pModel.ListItemData:
            if i['filePath'] == filePath:
                i['iconPath'] = iconPath
                i['mediaInfo'] = mediaInfo
                break
        self.supdate()

    def remove(self):
        print("This is remove22222222222!")
        self.pListView.removeItem(0)
        self.supdate()

    def removeall(self):
        print("This is removeall!")
        for i in range(len(self.pListView.m_pModel.ListItemData)):
            self.pListView.removeItem(0)
        self.supdate()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Please Select Your Footages", "",
                                                "All Files (*);;Media Files (*.mov,*.mp4,*.avi)", options=options)
        if files:
            return files

    def supdate(self):
        self.setFixedWidth(self.width() + 1)
        self.setFixedWidth(self.width() - 1)

    def getfilePathList(self):
        filePaths = []
        for i in self.pListView.m_pModel.ListItemData:
            try:
                filePaths.append(i['filePath'])
            except:
                pass
        return filePaths

    def toggleViewMode(self):
        print(self.pListView.viewMode())
        if self.pListView.viewMode() == QListView.ListMode:
            self.pListView.setViewMode(QListView.IconMode)
        else:
            self.pListView.setViewMode(QListView.ListMode)


class BackendThread(QThread):
    print('BackendThread')
    print(Example.updateList)
    update_date = pyqtSignal(str, str, str)

    def run(self):
        st = time.time()
        for filePath in Example.updateList:
            iconPath = pt.findThumb(filePath, "Temp/Cache")
            pt.findMediaInfo(filePath, "Temp/Cache")
            width, height, fps, duration = pt.findMediaInfo(filePath, "Temp/Cache")
            mediaInfo = "%(width)d x %(height)d  %(fps).02f\n%(duration)s" % {'width': width, 'height': height,
                                                                              'fps': fps, 'duration': duration}
            # print(mediaInfo)
            self.update_date.emit(filePath, iconPath, mediaInfo)
        et = time.time()
        print("Use Time to Load: %.4f\n" % (et - st))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyle("fusion")
    # app.setAttribute(Qt.AA_EnableHighDpiScaling)
    # if hasattr(QStyleFactory, 'AA_UseHighDpiPixmaps'):
    #     app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    mw = MainWindow()
    sys.exit(app.exec_())
