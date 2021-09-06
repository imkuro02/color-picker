import tkinter as tk
from tkinter import PhotoImage
import pyautogui
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from mss import mss
from math import floor
import tempfile
import pyperclip


def restrict(minval, val, maxval):
    if val < minval:
        return minval
    if val > maxval:
        return maxval
    return val

class Overlay:
    def __init__(self, parent):
        print(self, "created")
        self.parent = parent
        self.px_size = self.parent.px_size

        self.ZOOM_LEVEL_MOD = 2
        self.ZOOM_LEVEL_MAX = 20
        self.active = False
        self.zoom_level = 1  # set to lowest level
        self.screenshot_area_size = (self.zoom_level * self.ZOOM_LEVEL_MOD) + 1

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wait_visibility(self.root)
        self.root.configure(background="black")
        self.root.wm_attributes("-alpha", 0.002)
        self.root.attributes("-topmost", True)
        self.root.bind("<Button-1>", self.press_overlay)

        # windows 10
        self.root.bind("<MouseWheel>", self.modify_zoom_level)
        # x11
        self.root.bind("<Button-4>", self.modify_zoom_level)
        self.root.bind("<Button-5>", self.modify_zoom_level)

        self.root.config(cursor="crosshair")

        # make window invisible by calling set_active(False)
        self.set_active(False)

    # just a a func so event doesn't get passed to set_active
    def press_overlay(self, _event):
        self.set_active(False)
        self.screenshot()

    def modify_zoom_level(self, event=None):
        delta = 0
        if event is not None:
            delta = event.delta
            if event.num == 5:
                delta = 1
            if event.num == 4:
                delta = -1

        modifier = restrict(-1, int(delta), 1)
        self.zoom_level = restrict(1, self.zoom_level + modifier, self.ZOOM_LEVEL_MAX)
        self.screenshot_area_size = (self.zoom_level * self.ZOOM_LEVEL_MOD) + 1

    def set_active(self, val):
        #print(f"set active {val}")
        self.active = val
        if self.active:
            self.root.deiconify()
        else:
            self.root.withdraw()

    def screenshot(self):
        x, y = pyautogui.position()
        middle = floor(self.screenshot_area_size / 2)

        def cord_info(x_, y_):
            with mss() as sct:
                monitor = sct.monitors[0]
                clamped_x_ = restrict(
                    monitor["left"] + middle, x_, monitor["width"] - middle - 1
                )
                clamped_y_ = restrict(
                    monitor["top"] + middle, y_, monitor["height"] - middle - 1
                )
                # returns the actual coordinates and then coordinates that don't go outside of screen
                return x_, y_, clamped_x_, clamped_y_

        def get_screen(x_, y_):
            with mss() as sct:
                # set size of image
                rect = {
                    "left": x_ - floor(self.screenshot_area_size / 2),
                    "top": y_ - floor(self.screenshot_area_size / 2),
                    "width": self.screenshot_area_size,
                    "height": self.screenshot_area_size,
                }
                sct_img = sct.grab(rect)
                # Convert to PIL/Pillow Image
            return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        (
            x,
            y,
            clamped_x,
            clamped_y,
        ) = cord_info(x, y)
        diff_x = x - clamped_x
        diff_y = y - clamped_y

        img = get_screen(clamped_x, clamped_y)

        # get rgb of middle pixel
        color_rgb = img.load()[middle - diff_x, middle - diff_y]
        # color translation
        color_hex = '#%02x%02x%02x' % (color_rgb)
        r,g,b=color_rgb
        # setting color for parent
        self.parent.selected_color_rgb = color_rgb
        self.parent.selected_color_hex = color_hex
        # print(color_rgb,color_hex,x,y)

        # create a temp image and scale it
        temp_image = f"{self.parent.temp_dir.name}/img.gif"

        # apply a 10px border around whole image
        img = ImageOps.expand(img, border=10, fill="black")
        # crop it, using dark magic
        img = img.crop(
            (
                10 + diff_x,
                10 + diff_y,
                -10 + img.size[0] + diff_x,
                -10 + img.size[1] + diff_y,
            )
        )

        img = img.resize(
            (self.parent.preview_size, self.parent.preview_size), Image.NEAREST
        )

        # modify image with a crosshair
        draw = ImageDraw.Draw(img)
        preview_length = self.parent.preview_size
        preview_middle = floor(preview_length / 2)
        draw.line(
            (preview_middle, 0, preview_middle, preview_length), fill=128, width=3
        )
        draw.line(
            (0, preview_middle, preview_length, preview_middle), fill=128, width=3
        )

        # set the canvas to the preview image
        img.save(temp_image)
        self.img = PhotoImage(file=temp_image)
        # put image on canvas
        self.parent.root.preview_image.create_image(0, 0, anchor="nw", image=self.img)

    def update(self):
        if not self.active:
            print("overlay deactivated")
        else:
            x, y = pyautogui.position()
            self.root.geometry(f"600x600+{x - 300}+{y - 300}")
            self.screenshot()
            self.root.after(1, self.update)

    def start(self):
        if not self.active:
            print("setting active true, at start")
            self.set_active(True)
            self.root.after(1, self.update)


class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-topmost", 1)
        self.root.overrideredirect(True)
        self.root.wait_visibility(self.root)

        self.temp_dir = tempfile.TemporaryDirectory()
        print(self.temp_dir.name)

        self.selected_color_hex = ""
        self.selected_color_rgb = ""

        self.px_size = 25
        self.preview_image_canvas_size = 9
        self.preview_image = None

        # the size of the image preview
        self.preview_size = 200  # self.preview_image_canvas_size * self.px_size

        self.overlay = Overlay(self)

        self.root.geometry("200x400+1+1")
        self.root.button_quit = tk.Button(
            self.root, text="X", borderwidth=0, command=self.quit
        )
        self.root.button_quit.pack(side="top", anchor="ne")

        self.root.button_eye_drop = tk.Button(self.root, text="Eye Drop")
        self.root.button_eye_drop[
            "command"
        ] = lambda arg1=self.root: self.overlay.start()
        self.root.button_eye_drop.pack(side="top")

        # color value buttons
        self.root.label_color_rgb = tk.Button(self.root, text="rgb", borderwidth=0)
        self.root.label_color_rgb.pack(side="top")
        self.root.label_color_hex = tk.Button(self.root, text="hex", borderwidth=0)
        self.root.label_color_hex.pack(side="top")
        self.root.label_color_rgb["command"] = lambda arg1="rgb": self.copy_color_value(
            arg1
        )
        
        self.root.label_color_hex["command"] = lambda arg1="hex": self.copy_color_value(
            arg1
        )

        self.root.selected_color = tk.Canvas(
            self.root,
            width=self.preview_size,
            height=self.px_size,
            relief="ridge",
            bg="gray",
        )

        self.root.selected_color.pack(side="top")

        self.root.preview_image = tk.Canvas(
            self.root, width=self.preview_size, height=self.preview_size
        )
        self.root.preview_image.create_rectangle(
            0, 0, self.preview_size, self.preview_size, fill="gray"
        )
        self.root.preview_image.pack(side='bottom')

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.do_move)

        self.root.after(1, self.center)
        self.root.after(1, self.update)
        self.root.mainloop()

    def center(self):
        x, y = pyautogui.position()
        xmod = self.root.winfo_width()
        ymod = self.root.winfo_height()
        x = x - floor(xmod/2)
        y = y - floor(ymod/2)
        self.root.geometry(f"+{x}+{y}")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, _event):
        self.x = None
        self.y = None

    def do_move(self, event):
        delta_x = event.x - self.x
        delta_y = event.y - self.y
        x = self.root.winfo_x() + delta_x
        y = self.root.winfo_y() + delta_y
        self.root.geometry(f"+{x}+{y}")

    def copy_color_value(self, val):
        def decode(val_):
            if val_ == "rgb":
                return self.selected_color_rgb
            if val_ == "hex":
                return self.selected_color_hex

        pyperclip.copy(str(decode(val)))

    def update(self):
        if self.selected_color_hex != '':
            self.root.selected_color.config(bg=f"{self.selected_color_hex}")
            self.root.label_color_rgb.config(text=f"RGB {self.selected_color_rgb}")
            self.root.label_color_hex.config(text=f"HEX {self.selected_color_hex}")
        self.root.after(100, self.update)

    def quit(self):
        self.on_closing()

    def on_closing(self):
        self.overlay.active = False
        self.overlay.root.destroy()
        self.temp_dir.cleanup()
        self.root.destroy()


if __name__ == "__main__":
    Main()
