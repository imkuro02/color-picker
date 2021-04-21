from screeninfo import get_monitors
import pyautogui as pp


def getBorders():
    borders = []
    for m in get_monitors():
        borders.append((m.x,m.y,m.width,m.height))
    for border in borders:
        print(border)
    return(borders)

def getFocusedMonitor(borders,mouse_x,mouse_y):
    #focusedMonitor = -1
    for i, border in enumerate(borders):
        x, y, width, height = border
        if mouse_x >= x and mouse_y >= y and mouse_x <= x+width and mouse_y <= y+height:
            return i  
            

borders = getBorders()



if __name__ == '__main__':
    while True:
        monitor=getFocusedMonitor(borders,3551,1000)
        print(monitor)
        break
