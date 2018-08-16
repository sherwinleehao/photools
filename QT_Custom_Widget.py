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
###鼠标抬起时能回到之前鼠标消失的位置

###鼠标滚轮能对应操作

class Communicate(QObject):
    updateBW = pyqtSignal(int)

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.value = 5500
        self.w = 300
        self.h = 50
        self.r = 8
        self.inner = 4

        self.bar = QLabel("",self)
        self.bar.setGeometry(0,0,self.w,self.h)
        self.bar.setStyleSheet('background-color: rgba(128, 128, 128,128);border-width: 2px;border-style: solid;border-color: rgb(128, 128, 128);border-radius:%dpx;'%self.r)
        self.bar.setAlignment(Qt.AlignCenter)

        self.pointer = QLabel(self)
        self.pointer.setStyleSheet('background-color:rgba(0, 0, 0,255);border-radius:%dpx;'%(self.r-self.inner))
        self.pointer.setGeometry((self.w-(2*self.r))*(self.value/10000)+self.inner,self.inner,(self.r-self.inner)*2,(self.h-2*self.inner))

        self.num = QLabel(str(self.value/100),self)
        self.num.setFont(QFont("Microsoft YaHei", 15, QFont.Bold))
        self.num.setStyleSheet('color: white;background-color:None;border-width:0px;')
        self.num.setParent(self.bar)
        self.num.setAlignment(Qt.AlignCenter)
        self.num.setGeometry(int(self.w*0.25),int(0.1*self.h),int(self.w*0.5),int(0.8*self.h))
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 255))
        self.num.setGraphicsEffect(self.shadow)


    def updateUI(self):
        self.pointer.setGeometry((self.w - (2 * self.r)) * (self.value / 10000) + self.inner, self.inner,
                                 (self.r - self.inner) * 2, (self.h - 2 * self.inner))
        self.num.setText("%.2f"%(self.value/100))


    def setValue(self, value):
        self.value = value



class BurningWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)
        self.value = 75
        self.num = [75, 150, 225, 300, 375, 450, 525, 600, 675]

    def setValue(self, value):
        self.value = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        font = QFont("Serif", 7, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / 10.0))

        till = int(((w / 750.0) * self.value))
        full = int(((w / 750.0) * 700))

        if self.value >=700:
            qp.setPen(QColor(5, 255, 5))
            qp.setBrush(QColor(255, 0, 4))
            qp.drawRect(0, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till-full, h)
        else:
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, till, h)

        pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

        j = 0

        for i in range(step, 10*step, step):
            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            qp.drawText(i-fw/2, h/2, str(self.num[j]))
            j = j + 1

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.wid = TestWidget()
        # self.wid = BurningWidget()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.wid)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(0, 10000)
        sld.setValue(7500)
        sld.setGeometry(30, 40, 550, 30)
        sld.setGeometry(30, 390, 450, 30)
        self.c = Communicate()

        self.c.updateBW[int].connect(self.wid.setValue)
        sld.valueChanged[int].connect(self.changeValue)

        self.setGeometry(300, 300, 600, 210)
        self.setGeometry(300, 300, 990, 510)
        self.setWindowTitle("Burning widget")
        self.show()

    def changeValue(self, value):
        self.c.updateBW.emit(value)
        self.wid.updateUI()
        # self.wid.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())