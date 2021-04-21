import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget

app = QApplication(sys.argv)

widget = ... # define your widget
display_monitor = ... # the number of the monitor you want to display your widget

monitor = QDesktopWidget().screenGeometry(display_monitor)
widget.move(monitor.left(), monitor.top())
widget.showFullScreen()

