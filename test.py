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
###

class Communicate(QObject):
    updateBW = pyqtSignal(int)

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.setGeometry(300,300,500,400)
        self.bar = QLabel("BBBBB",self)
        self.bar.setGeometry(10,10,500,100)
        self.bar.setStyleSheet('background-color: red;border-radius:10px;')
        self.bar.setAlignment(Qt.AlignCenter)
        self.num = QLabel("NN",self)
        self.num.setParent(self.bar)
        self.num.setAlignment(Qt.AlignCenter)
        # self.num.setGeometry(10, 10, 500, 100)
        self.value = 75

    def setValue(self, value):
        self.value = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        width = self.value *5
        # qp.setPen(QColor(5, 255, 5))
        # qp.setBrush(QColor(255, 0, 4))
        # qp.drawRect(0, 0, width, 200)



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
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(1, 750)
        sld.setValue(75)
        sld.setGeometry(30, 390, 450, 30)

        self.c = Communicate()
        # self.wid = BurningWidget()
        self.wid = TestWidget()
        self.c.updateBW[int].connect(self.wid.setValue)

        sld.valueChanged[int].connect(self.changeValue)
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.wid)
        # vbox.addWidget(sld)
        hbox.addLayout(vbox)
        self.setLayout(hbox)


        self.setGeometry(300, 300, 990, 510)
        self.setWindowTitle("Burning widget")
        self.show()

    def changeValue(self, value):
        self.c.updateBW.emit(value)
        self.wid.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())