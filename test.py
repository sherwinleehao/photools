import sys
from PyQt5.QtWidgets import *
import time

class WinForm(QWidget):
    def __init__(self, parent = None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle('实时刷新页面例子')
        self.listFile = QListWidget()
        self.btnStart = QPushButton('开始')
        layout = QGridLayout(self)
        layout.addWidget(self.listFile, 0, 0, 1, 2)
        layout.addWidget(self.btnStart, 1, 1)

        self.btnStart.clicked.connect(self.slotAdd)
        self.setLayout(layout)

    def slotAdd(self):
        QApplication.processEvents()
        time.sleep(0.5)
        print("Sleep:0.5s")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = WinForm()
    form.show()
    sys.exit(app.exec_())