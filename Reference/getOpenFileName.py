from PyQt5.QtWidgets import QWidget,QPushButton,QFileDialog,QLineEdit,QApplication
import sys
class Example(QWidget):
   def __init__(self):
       super().__init__()
       self.initUI()
   def initUI(self):
       self.setGeometry(300,300,500,500)
       self.setWindowTitle('打开对话框！')
       self.bt1=QPushButton('打开文件',self)
       self.bt1.move(350,20)
       self.bt1.clicked.connect(self.OpenFileDialog)
       self.text=QLineEdit('路径',self)
       self.text.setGeometry(80,50,150,30)
       self.show()
   def OpenFileDialog(self):
       fname,ftype=QFileDialog.getOpenFileName(self,'打开文件','./')
       if fname[0]:
           self.text.setText(fname)
if __name__=='__main__':
   app=QApplication(sys.argv)
   ex=Example()
   exit(app.exec_())
