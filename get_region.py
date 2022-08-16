from turtle import width
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
    print(f"({p1[0]}, {p1[1]}), ", end='')
    while(keyboard.is_pressed('a') is True):
        time.sleep(.05)

def main():
    for i in range(1):
        get_pos()

if __name__ == '__main__':
    main()