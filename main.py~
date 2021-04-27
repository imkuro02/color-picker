import tkinter as tk
import pyautogui
import PIL.ImageGrab
from PIL import Image
from time import sleep

'''
MULTIPLIER_X
MULTIPLIER_Y

from screeninfo import get_monitors
for m in get_monitors():
        print(str(m))
'''

def getPx(event):

    x,y=pyautogui.position()
    root.attributes('-alpha',0.0)

    px = PIL.ImageGrab.grab(bbox=(x,y,x+1,y+1), include_layered_windows=False, all_screens=True)
    color = (px.load()[0,0])


    '''
    im.save('img.gif')
    im = Image.open('img.gif')
    im = im.convert('RGB')
    x,y=pyautogui.position()
    r, g, b = im.getpixel((x,y))
    color = (r, g, b)
    '''

    '''
    img = pyautogui.screenshot()
    img.save('img.png')
    i = Image.open('img.png')
    i.show()
    color = img.getpixel(pyautogui.position())
    '''

    root.attributes('-alpha',0.002)
    print(color,x,y)

def update():
    x,y=pyautogui.position()
    root.geometry(f'600x600+{x-300}+{y-300}')
    root.after(1,update)

# Create object

root = tk.Tk()

root.overrideredirect(True)

root.wait_visibility(root)

root.configure(background='black')

root.wm_attributes('-alpha',0.002)

root.geometry("500x500+1+1")

root.attributes('-topmost', True)

root.bind('<Button-1>', getPx)

root.config(cursor="crosshair")

root.after(1, update)

root.mainloop()
