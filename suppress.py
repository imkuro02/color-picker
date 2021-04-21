from pynput import mouse
import pyautogui

def on_move(x,y):
    pyautogui.moveTo(x,y,0.1)

def on_click(x,y,button,pressed):
    print('click')
    if button == mouse.Button.left:
        pass
    else:
        return(False)

def main():
    with mouse.Listener(on_move=on_move, on_click=on_click, suppress=True) as listener:
        listener.join()

main()
