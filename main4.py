import tkinter as tk
from tkinter import *  
import pyautogui
from PIL import Image
from PIL import ImageDraw
from mss import mss
from math import * 
from time import sleep
import io
import tempfile

class Overlay:
    def __init__(self,parent):
        self.parent = parent
        self.px_size = self.parent.px_size

        self.active = False
        self.screenshot_area_size = 9

        self.root = tk.Tk()


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
                rect = {
                        "left": x-floor(self.screenshot_area_size/2), 
                        "top": y-floor(self.screenshot_area_size/2), 
                        "width": self.screenshot_area_size, 
                        "height": self.screenshot_area_size
                        }

                sct_img = sct.grab(rect)
                # Convert to PIL/Pillow Image
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

        img = screenshot(x,y)
        middle = floor(self.screenshot_area_size/2)
        color_rgb = img.load()[middle,middle]

        color_hex = '#%02x%02x%02x' % (color_rgb)
        #print(color_rgb,color_hex,x,y)
        self.parent.root.selected_color.create_rectangle(0,0,self.px_size,self.px_size,fill=f'{color_hex}')

        temp_image = f'{self.parent.temp_dir.name}/img.gif'
        # print(temp_image)
        img_scale = self.px_size * self.screenshot_area_size
        img = img.resize((self.parent.preview_size,self.parent.preview_size),Image.NEAREST )

        draw = ImageDraw.Draw(img) 
        draw.line((self.parent.preview_size,self.parent.preview_size,0,0), fill=128, width=3)
        draw.line((0,self.parent.preview_size,self.parent.preview_size,0), fill=128, width=3)

        img = img.save(temp_image)
        self.img = PhotoImage(file=temp_image)
        self.parent.root.hover_color.create_image(0,0,anchor='nw', image=self.img)

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

        self.temp_dir = tempfile.TemporaryDirectory()
        print(self.temp_dir.name)

        self.px_size = 25
        self.hover_color_canvas_size = 9

        self.preview_size = self.hover_color_canvas_size * self.px_size

        self.overlay = Overlay(
                self,
                )

        self.root.geometry("250x350+1+1")

        self.root.button_eye_drop = tk.Button(self.root, text = 'Eye Drop', width = 25)
        self.root.button_eye_drop['command'] = lambda arg1 = self.root : self.overlay.start()
        self.root.button_eye_drop.pack()

        self.root.selected_color = tk.Canvas(self.root,width=self.px_size,height=self.px_size)
        self.root.selected_color.create_rectangle(0,0,self.px_size,self.px_size,fill='gray')
        self.root.selected_color.pack()

        self.root.hover_color = tk.Canvas(self.root,width=self.preview_size,height=self.preview_size)
        #self.root.hover_color.create_rectangle(0,0,25*100,25*10,fill='gray')
        self.root.hover_color.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.overlay.active = False
        self.overlay.root.destroy()
        self.temp_dir.cleanup()
        self.root.destroy()

def main():
    main = Main()

if __name__ == '__main__':
    main()
