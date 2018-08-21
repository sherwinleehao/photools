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
        pListView.setStyleSheet("QListView{icon-size:70px}")
        dic_list = {'listview': pListView, 'groupname': "我的好友"}
        pListView.setListMap(dic_list)
        self.addItem(pListView, "我的好友")
        self.show()

    def contextMenuEvent(self, event):
        pmenu = QMenu(self)
        pAddGroupAct = QAction("添加分组", pmenu)
        pmenu.addAction(pAddGroupAct)
        pAddGroupAct.triggered.connect(self.addGroupSlot)
        pmenu.popup(self.mapToGlobal(event.pos()))

    def addGroupSlot(self):
        groupname = QInputDialog.getText(self, "输入分组名", "")
        if groupname[0] and groupname[1]:
            pListView1 = ListView()
            pListView1.setViewMode(QListView.ListMode)
            pListView1.setStyleSheet("QListView{icon-size:70px}")
            self.addItem(pListView1, groupname[0])
            dic_list = {'listview': pListView1, 'groupname': groupname[0]}
            pListView1.setListMap(dic_list)
        elif groupname[0] == '' and groupname[1]:
            QMessageBox.warning(self, "警告", "我说你没有填写分组名哦~！")


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
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            pSubMenu = QMenu("转移联系人至", pmenu)
            pmenu.addMenu(pSubMenu)
            for item_dic in self.map_listview:
                pMoveAct = QAction(item_dic['groupname'], pmenu)
                pSubMenu.addAction(pMoveAct)
                pMoveAct.triggered.connect(self.move)
            pmenu.popup(self.mapToGlobal(event.pos()))

    def deleteItemSlot(self):
        index = self.currentIndex().row()
        if index > -1:
            self.m_pModel.deleteItem(index)

    def setListMap(self, listview):
        self.map_listview.append(listview)

    def addItem(self, pitem):
        self.m_pModel.addItem(pitem)

    def move(self):
        tolistview = self.find(self.sender().text())
        if tolistview is self:
            prelistview = self.sender().text()
            QMessageBox.warning(self, "警告", "该联系人就在{}，还怎么移动啊！".format(prelistview))
        else:
            index = self.currentIndex().row()
            pItem = self.m_pModel.getItem(index)
            tolistview.addItem(pItem)
            self.m_pModel.deleteItem(index)

    def find(self, pmenuname):
        for item_dic in self.map_listview:
            if item_dic['groupname'] == pmenuname:
                return item_dic['listview']


class ListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.ListItemData = []
        self.Data_init()

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
        randomnum = random.sample(range(26), 10)
        for i in randomnum:
            # randname = Random_Name.getname()
            # randname = str(uuid.uuid4())
            randname = str("Sherwin lee")
        ItemData = {'name': '', 'iconPath': ''}
        ItemData['name'] = randname
        ItemData['iconPath'] = "./res/" + str(i) + ".jpg"
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
        Vbox = QVBoxLayout()
        Vbox.addWidget(LM)
        self.setLayout(Vbox)
        # print(LM.data)
        self.setGeometry(100, 100, 360, 720)
        self.setWindowTitle("Pre-Research")



        self.show()

    def mousePressEvent(self, QMouseEvent):
        print('PPPPPPP')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


