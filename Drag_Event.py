# coding=utf-8

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget, QWidget, QLineEdit, QDateTimeEdit, QVBoxLayout, QHBoxLayout \
        , QGridLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, QDateTime, QMimeData, QUrl
import sys

class MainWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vlayout = QVBoxLayout()
        grid = QGridLayout()
        label1 = QLabel('文件路径')
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedHeight(40)
        grid.addWidget(label1, 0, 0)
        grid.addWidget(self.lineEdit, 0, 1, )
        vlayout.addLayout(grid)
        vlayout.addStretch(1)
        self.setLayout(vlayout)
        self.setAcceptDrops(True)

    def enableBorder(self, enable):
        if enable:
            # self.setStyleSheet("MainWidget{border:3px solid green}")
            self.setStyleSheet("MainWidget{border:3px solid #165E23}")
        else:
            self.setStyleSheet('')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.enableBorder(True)
        else:
            event.ignore()
            # super(self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.LinkAction)
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        print('dragLeaveEvent...')
        self.enableBorder(False)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            # 遍历输出拖动进来的所有文件路径
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                print(path)
            text = event.mimeData().text()
            self.lineEdit.setText(text)
            event.acceptProposedAction()
            self.enableBorder(False)
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec_())
