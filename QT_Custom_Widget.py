import sys
from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


###控件中间显示小数点后两位的数值
###鼠标进入控件后开始变成左右的光标
###鼠标按下拖拽时，鼠标消失，游标高亮，控件边缘高亮
###鼠标拖拽能偏移数值及游标位置
###鼠标滚轮能对应操作
###鼠标抬起时能回到之前鼠标消失的位置
###鼠标右键单击能将值设置为默认值

###拖拽控件 能修改旁边label的值
###面板内放置多个控件及label，相互不干扰

class Communicate(QObject):
    valueChanged = pyqtSignal(int)

class TestWidget(QWidget):
    valueChanged = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.name = "Slider"
        self.default = 5000
        self.value = 5000
        self.w = 300
        self.h = 90
        self.r = 8
        self.title_h = 30
        self.inner = 6
        self.oldPosX = 0
        self.oldPosY = 0


        self.container = QLabel("",self)
        self.container.setGeometry(0, 0, self.w, self.h)
        # self.container.setStyleSheet('background-color: rgb(128, 0, 0)')
        self.container.setAlignment(Qt.AlignCenter)

        self.title = QLabel(self.name,self)
        self.title.setParent(self.container)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Microsoft YaHei", 8))
        self.title.setStyleSheet('color: red')
        self.title.setGeometry(int(self.w * 0.25), 0, int(self.w * 0.5),self.title_h)

        self.bar = QLabel("",self)
        self.bar.setGeometry(0,self.title_h,self.w,(self.h-self.title_h))
        self.bar.setStyleSheet('background-color: rgba(128, 128, 128,128);border-width: 2px;border-style: solid;border-color: rgb(128, 128, 128);border-radius:%dpx;'%self.r)
        self.bar.setAlignment(Qt.AlignCenter)

        self.pointer = QLabel(self)
        self.pointer.setStyleSheet('background-color:rgba(0, 255, 0,255);border-radius:%dpx;'%(self.r-self.inner))
        self.pointer.setGeometry((self.w-(2*self.r))*(self.value/10000)+self.inner,self.inner+self.title_h,(self.r-self.inner)*2,((self.h-self.title_h)-2*self.inner))

        self.num = QLabel(str(self.value/100),self)
        self.num.setFont(QFont("Microsoft YaHei", 15, QFont.Bold))
        self.num.setStyleSheet('color: white;background-color:None;border-width:0px;')
        self.num.setParent(self.bar)
        self.num.setAlignment(Qt.AlignCenter)
        self.num.setGeometry(int(self.w*0.25),int(0.1*(self.h-self.title_h)),int(self.w*0.5),int(0.8*(self.h-self.title_h)))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 64))
        self.num.setGraphicsEffect(self.shadow)

        self.bar.setCursor(Qt.SizeHorCursor)
        self.pointer.setCursor(Qt.SizeHorCursor)

    def updateUI(self):
        self.pointer.setGeometry((self.w - (2 * self.r)) * (self.value / 10000) + self.inner, self.inner + self.title_h,
                                 (self.r - self.inner) * 2, ((self.h - self.title_h) - 2 * self.inner))
        self.num.setText("%.2f"%(self.value/100))

    def setValue(self, value):
        if value > 10000:
            value = 10000
        elif value <0:
            value = 0
        self.value = value
        self.updateUI()
        self.valueChanged.emit(self.value)


    def mousePressEvent(self, e):
        if e.button() == 1:
            self.oldPosX = e.pos().x()
            self.oldPosY = e.pos().y()
            # print("Mouse Down Pos :",self.oldPosX,self.oldPosY)
            self.bar.setStyleSheet('background-color: rgba(128, 128, 128,128);border-width: 2px;border-style: solid;border-color: rgb(255, 128, 128);border-radius:%dpx;'%self.r)
            self.bar.setCursor(Qt.BlankCursor)
        elif e.button() == 2:
            self.setValue(self.default)

    def mouseMoveEvent(self, e):
            self.deltaX = e.pos().x()-self.oldPosX
            self.deltaY = e.pos().y()-self.oldPosY
            self.oldPosX = e.pos().x()
            self.oldPosY = e.pos().y()
            # print("Mouse Delta Pos :",self.deltaX,self.deltaY)
            self.setValue(self.value + self.deltaX*30)
            self.bar.setCursor(Qt.BlankCursor)

    def mouseReleaseEvent(self, e):
        self.oldPosX = 0
        self.oldPosY = 0
        # print("Mouse Up Pos :",self.oldPosX,self.oldPosY)
        self.bar.setStyleSheet('background-color: rgba(128, 128, 128,128);border-width: 2px;border-style: solid;border-color: rgb(128, 128, 128);border-radius:%dpx;'%self.r)
        self.bar.setCursor(Qt.SizeHorCursor)

    def wheelEvent(self, e):
        angle = e.angleDelta() / 8
        angleX = angle.x()
        angleY = angle.y()
        print(angleX,angleY)
        self.setValue(self.value + angleY * 10)

    def setTitle(self,newTitle):
        self.title.setText(newTitle)

    # def enterEvent(self, e):
    #     print("mouse enter!",self.name)
    #
    # def leaveEvent(self, e):
    #     print("mouse leave!",self.name)


class Example(QWidget):
    # sldSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        wid = TestWidget()
        wid.setTitle('Hue')
        wid2 = TestWidget()
        wid2.setTitle('Saturation')
        wid3 = TestWidget()
        wid3.setTitle('Lumemass')
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(wid)
        vbox.addWidget(wid2)
        vbox.addWidget(wid3)
        hbox.addLayout(vbox)

        showbox0 = QLabel("12.34",self)
        showbox1 = QLabel("23.45",self)
        showbox2 = QLabel("34.56",self)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(showbox0)
        vbox2.addWidget(showbox1)
        vbox2.addWidget(showbox2)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)

        wid.valueChanged[int].connect(self.changeValue)


        self.setGeometry(300, 300, 600, 210)
        self.setGeometry(300, 300, 990, 510)
        self.setWindowTitle("Burning widget")
        self.show()

    def changeValue(self, value):
        print(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())