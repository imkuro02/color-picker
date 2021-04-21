import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):      

        cb = QtWidgets.QPushButton('Switch', self)
        cb.move(20, 20)
        cb.clicked.connect(self.add_entry)
        self.setGeometry(300, 300, 250, 150)
        self.show()

    def add_entry(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
