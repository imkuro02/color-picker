import tkinter as tk
import pyautogui
from PIL import Image
from mss import mss
from time import sleep

class Overlay:
    def __init__(self,parent):
        self.parent = parent

        self.root = tk.Tk()

        self.active = False

        self.root.overrideredirect(True)
        self.root.wait_visibility(self.root)
        self.root.configure(background='black')
        self.root.wm_attributes('-alpha',0.002)
        #self.root.geometry("500x500+1+1")
        self.root.attributes('-topmost', True)
        self.root.bind('<Button-1>', self.press_overlay)
        self.root.config(cursor="crosshair")

        self.set_active(False)

    # just a a func so event doesn't get passed to set_active
    def press_overlay(self, event):
        self.set_active(False)
        self.get_px()

    def set_active(self,val):
        print(f'set active {val}')
        self.active = val
        
        if self.active:
            self.root.deiconify()
        else:
            self.root.withdraw()

    def get_px(self):
        x,y=pyautogui.position()
        #self.root.attributes('-alpha',0.0)
        def screenshot(x,y):
            with mss() as sct:
                monitor = sct.monitors[0]
                rect = {"left": x, "top": y, "width": 1, "height": 1}
                sct_img = sct.grab(rect)
                # Convert to PIL/Pillow Image
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        try:
            color_rgb = screenshot(x,y).load()[0,0]
            color_hex = '#%02x%02x%02x' % (color_rgb)
            print(color_rgb,color_hex,x,y)
            self.parent.selected_color.create_rectangle(0,0,25,25,fill=f'{color_hex}')
        except ValueError:
            print('screenshot messed up')

    def update(self):
        if not self.active:
            print('overlay deactivated')
        else:
            x,y=pyautogui.position()
            self.root.geometry(f'600x600+{x-300}+{y-300}')
            self.get_px()
            self.root.after(1,self.update)

    def start(self):
        self.set_active(True)
        self.root.after(1,self.update)

class Main:
    def __init__(self):
        self.root = tk.Tk()

        self.overlay = Overlay(self.root)

        self.root.geometry("250x350+1+1")

        self.root.button_eye_drop = tk.Button(self.root, text = 'Eye Drop', width = 25)
        self.root.button_eye_drop['command'] = lambda arg1 = self.root : self.overlay.start()
        self.root.button_eye_drop.pack()

        self.root.selected_color = tk.Canvas(self.root,width=25,height=25)
        self.root.selected_color.create_rectangle(0,0,25,25,fill='gray')
        self.root.selected_color.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.overlay.active = False
        self.overlay.root.destroy()
        self.root.destroy()

def main():
    main = Main()

if __name__ == '__main__':
    main()
