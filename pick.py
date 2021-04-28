from mss import mss
from PIL import Image
from PIL import ImageGrab
import PIL

import datetime

def a():
    # Capture entire screen
    def aa():
        with mss() as sct:
            monitor = sct.monitors[0]
            rect = {"left": -30, "top": 0, "width": 100, "height": 100}
            sct_img = sct.grab(rect)
            # Convert to PIL/Pillow Image
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    col = aa().load()[0,0]
    #print(col)

def b():
    x = 0
    y = 0
    px = PIL.ImageGrab.grab(bbox=(x,y,x+1,y+1), include_layered_windows=False, all_screens=True)
    color_rgb = (px.load()[0,0])
    #print(color_rgb)

x = 1
start = datetime.datetime.now()
for i in range(x):
    a()

print(datetime.datetime.now()-start)

start = datetime.datetime.now()
for i in range(x):
    b()

print(datetime.datetime.now()-start)

