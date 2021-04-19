import pyautogui
from PIL import ImageGrab

from pynput import mouse

def getCords():

    def on_click(x, y, button, pressed):
        if button == mouse.Button.left:
            print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
            listener.stop()
        else:
            print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()
    x, y = pyautogui.position()
    return(x,y)

def getPixel(x,y):
    cords = (x,y,x+1,y+1)
    box = cords 
    pixel = ImageGrab.grab(box)
    print(pixel.getpixel((0,0)))

#pixel.show()

x, y = getCords()
print(f'cords : {x},{y}')
print(getPixel(x,y))

