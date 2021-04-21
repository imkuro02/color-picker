import tkinter as tk
from time import *

app = tk.Tk()

class Overlay:

    def __init__(self,x=1,y=1):
        self.x = x
        self.y = y

    def move(app,x,y):
        app.geometry(f'+{x}+{y}')

    app.title('color-picker-overlay')
    app.geometry('300x300')
    app.wm_attributes('-alpha',0.8)
    app.mainloop()

overlay = Overlay(1,1)

sleep(1)

overlay.move(200,200)

sleep(1)

overlay(400,400)


