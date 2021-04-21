import pyautogui
from PIL import ImageGrab
from pynput import mouse
import threading
from tkinter import *

def getCords():
    def on_move(x,y):
        pass
        #pyautogui.position = (x,y)
    def on_click(x, y, button, pressed):
        if button == mouse.Button.left:
            print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
        else:
            print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))
            return False

    with mouse.Listener(on_move=on_move,on_click=on_click, suppress=False) as listener:
        listener.join()
    x, y = pyautogui.position()
    return(x,y)

def getPixel(x,y):
    cords = (x,y,x+1,y+1)
    box = cords 
    pixel = ImageGrab.grab(box)
    print(pixel.getpixel((0,0)))

def mouseLock(window,lock):
    while True:
        if lock:
            x, y = window.winfo_rootx(), window.winfo_rooty()
            pyautogui.moveTo(x,y)

window=Tk()
btn=Button(window, text="pick col", fg='blue')
btn.place(x=80, y=100)
window.title('color picker')
window.geometry("300x200+500+500")
mouseLockThread = threading.Thread(target=mouseLock, args=(window,True,))
mouseLockThread.start()
window.mainloop()

print('tk scuks cuck')




