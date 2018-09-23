# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QPixmap, QPalette, QBrush
# from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
# import PyQt5
# from PyQt5.QtCore import Qt
#
#
# class Example2(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         previousBtn = QPushButton('Previous')
#         nextBtn = QPushButton('Next')
#
#         hbox = QHBoxLayout()
#         hbox.addWidget(previousBtn)
#         hbox.addStretch(1)
#         hbox.addWidget(nextBtn)
#
#         vbox = QVBoxLayout()
#         vbox.addLayout(hbox)
#
#         nextBtn.clicked.connect(self.next_Img)
#         previousBtn.clicked.connect(self.previous_Img)
#
#         self.setLayout(vbox)
#         self.setGeometry(100, 100, 512, 512)
#         self.setWindowTitle('Set IMG')
#         self.show()
#
#     def next_Img(self, event):
#         print("This is next Button")
#         palette1 = QPalette()
#         palette1.setBrush(self.backgroundRole(), QBrush(QPixmap("img\\04.jpg")))  # 设置背景图片
#         self.setPalette(palette1)
#
#     def previous_Img(self, event):
#         print("This is next Button")
#         palette1 = QPalette()
#         palette1.setBrush(self.backgroundRole(), QBrush(QPixmap("img\\03.jpg")))  # 设置背景图片
#         self.setPalette(palette1)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     example2 = Example2()
#     sys.exit(app.exec_())



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowModality(QtCore.Qt.WindowModal)
        mainWindow.resize(624, 511)
        self.centralWidget = QtWidgets.QWidget(mainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(-500, 0, 1280, 720))
        self.label.setText("一颗数据小白菜")
        self.label.setObjectName("label")
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setPixmap(QtGui.QPixmap("img\\01.jpg"))
        # self.label.setScaledContents(True)
        mainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle('您好')
        mainWindow.setWindowIcon(QIcon('logo.png'))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())