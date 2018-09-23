import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
import PyQt5
from PyQt5.QtCore import Qt


class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        previousBtn = QPushButton('Previous')
        nextBtn = QPushButton('Next')

        # pixmap = QPixmap("img\\01.jpg")
        # lbl = QLabel(self)
        # lbl.setPixmap(pixmap)

        hbox = QHBoxLayout()
        hbox.addWidget(previousBtn)
        hbox.addStretch(1)
        # hbox.addWidget(lbl)
        hbox.addWidget(nextBtn)

        vbox = QVBoxLayout()
        # vbox.addStretch(1)
        vbox.addLayout(hbox)
        # vbox.addStretch(1)

        # photo =  QPixmap("img\\01.jpg")
        # # lable1 = QLabel(self)
        # lable3 = QLabel(self)
        # # lable1.setText("文本标签")
        # # lable1.setAutoFillBackground(True)
        # # palette = QPalette()
        # # palette.setColor(QPalette.Window, Qt.red)
        # # lable1.setPalette(palette)
        # # lable1.setAlignment(Qt.AlignCenter)
        # # lable3.setToolTip("这个一个图片标签")
        # lable3.setPixmap(photo)
        # vbox.addWidget(lable3)

        nextBtn.clicked.connect(self.next_Img)
        previousBtn.clicked.connect(self.previous_Img)
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap("img\\01.jpg")))  # 设置背景图片
        self.setPalette(palette1)

        self.setLayout(vbox)
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle('箱布局')
        self.show()
        pass

    def next_Img(self, event):
        print("This is next Button")
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap("img\\04.jpg")))  # 设置背景图片
        self.setPalette(palette1)

    def previous_Img(self, event):
        print("This is next Button")
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap("img\\03.jpg")))  # 设置背景图片
        self.setPalette(palette1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example2 = Example2()
    sys.exit(app.exec_())
