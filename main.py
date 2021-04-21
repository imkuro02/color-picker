from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import sys
import screenInfo as si
from time import sleep
import pyautogui
import threading

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def followCursor(self):
        prev_focused_monitor = -1
        borders=si.getBorders()
        def refreshOverlay():
            # on dwm hiding and unhiding moves the window to correct screen
            self.hide()
            #self.move(0,0)
            self.showNormal()
            self.showFullScreen()
        while True:
            sleep(0.1)
            x,y=pyautogui.position()
            focused_monitor=si.getFocusedMonitor(borders,x,y)
            if focused_monitor != prev_focused_monitor:
                prev_focused_monitor = focused_monitor
                refreshOverlay()

    def add_entry(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()
       # self.hide()
     
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")

        cb = QPushButton('Switch', self)
        cb.clicked.connect(self.add_entry)

        #layout.addWidget(self.label)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 500, 500)
        self.setWindowOpacity(0.5)
        self.setLayout(layout)
        
        t = threading.Thread(target=self.followCursor)
        t.start()

class MainWindow(QMainWindow):
    w=[0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        for i in range(1):
            self.w[i] = AnotherWindow()
            self.w[i].show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
