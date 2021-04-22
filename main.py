from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import sys
import screenInfo as si
from time import sleep
import pyautogui
import threading
class AnotherWindow(QMainWindow):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def refreshOverlay(self):
        # on dwm hiding and unhiding moves the window to correct screen
        self.showNormal()
        x,y=pyautogui.position()
        # xx , yy corner cords of current focus display
        xx, yy = si.getFocusedMonitor(self.screen_borders,x,y)
        self.move(xx,yy)
        self.hide() 
        self.showFullScreen()
        #self.add_entry()
    '''
    def checkMonitor(self):
        prev_focused_monitor = -1
        borders=si.getBorders()
        while True:
            sleep(.3)
            x,y=pyautogui.position()
            focused_monitor=si.getFocusedMonitor(borders,x,y)
            if focused_monitor != prev_focused_monitor:
                prev_focused_monitor = focused_monitor
                self.refreshOverlay(x,y)
    ''' 
    '''
    def add_entry(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()
       # self.hide()
    '''  

    class MouseArea(QPushButton):
        def __init__(self, parent=None):
            super(QPushButton, self).__init__(parent)
            self.parent=parent
        '''
        def enterEvent(self,QEvent):
            print('entered')
        '''
        def leaveEvent(self,QEvent):
            self.parent.refreshOverlay()


    def __init__(self):
        super().__init__()
        #layout = QVBoxLayout()
        self.screen_borders = si.getBorders()
        layoutGrid = QGridLayout()
        self.setLayout(layoutGrid)
        self.label = QLabel("Another Window")

        '''
        cb = QPushButton('Switch', self)
        cb.clicked.connect(self.add_entry)
        '''

        self.mouseArea = self.MouseArea(self)
        #self.mouseArea.resize(2600,1500)
        self.setCentralWidget(self.mouseArea)
    

        #layout.addWidget(self.label)
        
        self.setGeometry(0, 0, 500, 500)
        self.setWindowOpacity(0.1)
        #self.setLayout(layout)
        
        #self.followCursor()




class MainWindow(QMainWindow):
    w=[0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)
    
    def mouseMoveEvent(self, e):
        self.move(e.x.e.y)
    def show_new_window(self, checked):
        for i in range(1):
            self.w[i] = AnotherWindow()
            self.w[i].show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
