#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee
Website: Sherwinleehao.com
Last edited: 20180906

Task:


# 加入Add More和Remove，Remove All的按钮
#     添加多个文件到列表
    删除选中的文件
    # 删除全部文件
    # 弹窗显示已经在列表内的item

# 加载资源应该先加载占位缩略图，然后开启线程进行后台加载缩略图并替换

# 显示两行信息，文件名\n分辨率，帧率，
图片仅显示分辨率

修改列表缩略图的列表样式，修改滑动栏的样式，列表样式
做加载过程的占位GIF，完成后显示真缩图，缩略图将以MD5形式命名并缓存
视频文件后台获取25张图，划过能动态显示视频

鼠标悬停的Item上有删除按键


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

    def parseItem(self,item):
        name = item['name']
        # iconPath = item['iconPath']
        # filePath = item['filePath']
        mediaInfo = item['mediaInfo']
        tempStr = name+"\n"+mediaInfo
        print(tempStr)
        return tempStr

class Example(QWidget):
    updateList = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pListView = ListView()
        self.pListView.setViewMode(QListView.ListMode)
        self.pListView.setStyleSheet("QListView{icon-size:120px}")

        self.btn_tester = QPushButton("tester", self)
        self.btn_addmore = QPushButton("Add More", self)
        # self.btn_remove = QPushButton("Remove", self)
        self.btn_removeall = QPushButton("Remove All", self)

        Hbox = QHBoxLayout()
        Hbox.addWidget(self.btn_addmore)
        Hbox.addStretch(1)
        # Hbox.addWidget(self.btn_remove)
        Hbox.addWidget(self.btn_removeall)

        Vbox = QVBoxLayout()
        Vbox.addLayout(Hbox)
        Vbox.addWidget(self.pListView)
        Vbox.addWidget(self.btn_tester)
        self.setLayout(Vbox)
        self.setGeometry(300, 300, 360, 720)
        self.setWindowTitle("Pre-Research")
        self.btn_tester.clicked.connect(self.tester)
        self.btn_addmore.clicked.connect(self.addmore)
        # self.btn_remove.clicked.connect(self.remove)
        self.btn_removeall.clicked.connect(self.removeall)
        self.show()

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

    def updateThumb(self,filePath,iconPath,mediaInfo):
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

    def tester(self):
        print("This is Tester!")
        print(self.pListView.m_pModel.ListItemData)



class BackendThread(QThread):
    print('BackendThread')
    print(Example.updateList)
    update_date = pyqtSignal(str,str,str)
    def run(self):
        st = time.time()
        for filePath in Example.updateList:
            iconPath = pt.findThumb(filePath,"Temp/Cache")
            pt.findMediaInfo(filePath, "Temp/Cache")
            width, height, fps, duration = pt.findMediaInfo(filePath,"Temp/Cache")
            mediaInfo = "%(width)d x %(height)d  %(fps).03f\n%(duration)s" % {'width':width, 'height':height, 'fps':fps, 'duration':duration}
            # print(mediaInfo)
            self.update_date.emit(filePath, iconPath, mediaInfo)
        et = time.time()
        print("Use Time to Load: %.4f\n"%(et-st))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # shutil.rmtree('Temp')
    ex = Example()
    sys.exit(app.exec_())
