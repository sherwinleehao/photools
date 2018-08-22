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
import os,random
import uuid


class QQ(QToolBox):
    def __init__(self):
        super().__init__()
        pListView = ListView()

        pListView.setViewMode(QListView.ListMode)
        pListView.setStyleSheet("QListView{icon-size:120px}")
        self.addItem(pListView, "我的好友2")
        print('pListView',pListView)
        self.show()



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
            pDeleteAct.setShortcut('Ctrl+L')
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            pmenu.addAction(pDeleteAct)

            pDeleteAct2 = QAction("22222222", pmenu)
            pmenu.addAction(pDeleteAct2)


            pMenu = QAction("转移联系人至", pmenu)
            pmenu.addAction(pMenu)
            pmenu.popup(self.mapToGlobal(event.pos()))

    def deleteItemSlot(self):
        index = self.currentIndex().row()
        if index > -1:
            self.m_pModel.deleteItem(index)

    # def setListMap(self, listview):
    #     self.map_listview.append(listview)

    def addItem(self, pitem):
        self.m_pModel.addItem(pitem)


    # def find(self, pmenuname):
    #     for item_dic in self.map_listview:
    #         if item_dic['groupname'] == pmenuname:
    #             return item_dic['listview']
    #

class ListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.ListItemData = []
        self.Data_init()
        print(self.ListItemData)

    def data(self, index, role):
        if index.isValid() or (0 <= index.row() < len(self.ListItemData)):
            if role == Qt.DisplayRole:
                return QVariant(self.ListItemData[index.row()]['name'])
            elif role == Qt.DecorationRole:
                return QVariant(QIcon(self.ListItemData[index.row()]['iconPath']))
            elif role == Qt.SizeHintRole:
                return QVariant(QSize(70, 80))
            elif role == Qt.TextAlignmentRole:
                return QVariant(int(Qt.AlignHCenter | Qt.AlignVCenter))
            elif role == Qt.FontRole:
                font = QFont()
                font.setPixelSize(20)
                return QVariant(font)

        else:
            return QVariant()

    def rowCount(self, parent=QModelIndex()):
        return len(self.ListItemData)

    def Data_init(self):
        randomnum = random.sample(range(100), 30)
        for i in randomnum:
            randname = str("Sherwin %d"%i)
            ItemData = {'name': '', 'iconPath': ''}
            ItemData['name'] = randname
            ItemData['iconPath'] = "img/thumb/thumb_%04d.jpg"%i
            self.ListItemData.append(ItemData)

    def addItem(self, itemData):
        if itemData:
            self.beginInsertRows(QModelIndex(), len(self.ListItemData), len(self.ListItemData) + 1)
            self.ListItemData.append(itemData)
            self.endInsertRows()

    def deleteItem(self, index):
        del self.ListItemData[index]

    def getItem(self, index):
        if index > -1 and index < len(self.ListItemData):
            return self.ListItemData[index]



class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        LM = QQ()
        tester = QPushButton("tester",self)
        Vbox = QVBoxLayout()
        Vbox.addWidget(LM)
        Vbox.addWidget(tester)
        self.setLayout(Vbox)
        self.setGeometry(-600, 300, 360, 720)
        self.setWindowTitle("Pre-Research")

        tester.clicked.connect(self.tester)

        self.show()

    def tester(self):
        print("This is Tester!")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


