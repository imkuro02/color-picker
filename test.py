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


def screenshot():

    def get_screen():
        with mss() as sct:
            monitor = sct.monitors[1]
            print(sct.monitors)
            print(monitor)
            # set size of image
            rect = {
                    "left": 0,
                    "top": 1,
                    "width": 100,
                    "height": 100
                    }
            sct_img = sct.grab(rect)
            # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    get_screen()
screenshot()
