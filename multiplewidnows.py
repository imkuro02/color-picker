from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import sys


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def add_entry(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()
     
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")

        cb = QPushButton('Switch', self)
        cb.clicked.connect(self.add_entry)

        #layout.addWidget(self.label)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 400, 300)
        self.setWindowOpacity(0.5)
        self.setLayout(layout)
        

class MainWindow(QMainWindow):
    w=[0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        for i in range(2):
            self.w[i] = AnotherWindow()
            self.w[i].show()
            print('showing new win')


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
