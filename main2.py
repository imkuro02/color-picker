import tkinter as tk
import pyautogui
import PIL.ImageGrab
from PIL import Image
from time import sleep

def create_overlay(root):

    def get_px(event):
        x,y=pyautogui.position()
        overlay.attributes('-alpha',0.0)

        px = PIL.ImageGrab.grab(bbox=(x,y,x+1,y+1), include_layered_windows=False, all_screens=True)

        overlay.attributes('-alpha',0.002)
        overlay.destroy()

        color_rgb = (px.load()[0,0])
        color_hex = '#%02x%02x%02x' % (color_rgb)
        print(color_rgb,color_hex,x,y)

        root.selected_color.create_rectangle(0,0,25,25,fill=f'{color_hex}')

    def update():
        x,y=pyautogui.position()
        overlay.geometry(f'600x600+{x-300}+{y-300}')
        overlay.after(1,update)

    overlay = tk.Tk()
    overlay.overrideredirect(True)
    overlay.wait_visibility(overlay)
    overlay.configure(background='black')
    overlay.wm_attributes('-alpha',0.002)
    #overlay.geometry("500x500+1+1")
    overlay.attributes('-topmost', True)
    overlay.bind('<Button-1>', get_px)
    overlay.config(cursor="crosshair")
    overlay.after(1,update)

def main():
    root = tk.Tk()
    root.geometry("250x350+1+1")

    root.button_eye_drop = tk.Button(root, text = 'Eye Drop', width = 25)
    root.button_eye_drop['command'] = lambda arg1 = root : create_overlay(arg1)
    root.button_eye_drop.pack()

    root.selected_color = tk.Canvas(root,width=25,height=25)
    root.selected_color.create_rectangle(0,0,25,25,fill='gray')
    root.selected_color.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
