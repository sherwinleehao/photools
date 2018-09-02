import  sys
from  PyQt5.QtWidgets import QWidget,QPushButton,QMessageBox,QLineEdit,QApplication
from random import randint #引入产生随机数
class Example(QWidget):
    def __init__(self):
       super().__init__()
       self.initUI()
    def initUI(self):
        self.setGeometry(300,300,300,220)
        self.setWindowTitle('学习编程把--猜数字')
        self.bt1=QPushButton('我猜',self)
        self.bt1.setGeometry(115,150,70,30)
        self.bt1.setToolTip('在这里输入数字')
        self.bt1.clicked.connect(self.showMessage) #信号连接
        self.text=QLineEdit('在这里输入数字',self)
        self.text.selectAll()
        self.text.setFocus()
        self.text.setGeometry(80,50,150,30)
        self.show()
    def showMessage(self):
      QMessageBox.about(self,'我猜我猜我猜猜猜','nihao')#2个参数 文本框标题 ，文本内容
      self.text.clear()
      self.text.setFocus()
if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())