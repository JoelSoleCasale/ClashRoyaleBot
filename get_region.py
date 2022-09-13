#Debugging script to esasly get regions and positions on screen

import pyautogui as pg
import keyboard
import time

def get_region():
    while(keyboard.is_pressed('a') is False):
        time.sleep(.05)
    p1 = pg.position()
    print(p1)
    while(keyboard.is_pressed('a') is True):
        time.sleep(.05)
    while(keyboard.is_pressed('a') is False):
        time.sleep(.05)
    p2 = pg.position()
    print(p2)
    width, height = p2[0]-p1[0], p2[1]-p1[1]
    print(f"the rectangle area is: ({p1[0]}, {p1[1]}, {width}, {height})")

def get_pos():
    while(keyboard.is_pressed('a') is False):
        time.sleep(.05)
    p1 = pg.position()
    px = pg.pixel(p1[0], p1[1])
    print(f"({p1[0]}, {p1[1]}), ", end="")
    # print(f"[({p1[0]}, {p1[1]}), ({px[0]}, {px[1]}, {px[2]})], ", end="")
    while(keyboard.is_pressed('a') is True):
        time.sleep(.05)

def main():
    for i in range(20):
        get_pos()

if __name__ == '__main__':
    main()