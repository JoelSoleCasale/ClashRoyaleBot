# Debugging script to esasly get regions and positions on screen
import random, win32gui, os
import pyautogui as pg
import keyboard
import time

import gameBoard

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

def correct_window():
    '''The BlueStacks window must be fullHD, and with the correct with and heigh'''
    hwnd = win32gui.FindWindow(None, "BlueStacks App Player")
    rect = list(win32gui.GetWindowRect(hwnd))
    win32gui.MoveWindow(hwnd, rect[0], rect[1], 637, 1108, True)

def get_pos():
    while(keyboard.is_pressed('a') is False):
        time.sleep(.05)
    p1 = pg.position()
    px = pg.pixel(p1[0], p1[1])
    print(f"({p1[0]}, {p1[1]}), ", end="")
    # print(f"[({p1[0]}, {p1[1]}), ({px[0]}, {px[1]}, {px[2]})], ", end="")
    while(keyboard.is_pressed('a') is True):
        time.sleep(.05)

def _get_window_rect(name="BlueStacks App Player"):
        '''returns a list with the coordinates and dimensions, returns [x, y, w, h]'''
        rect = list(win32gui.GetWindowRect(win32gui.FindWindow(None, "BlueStacks App Player")))
        rect[2] -= rect[0]
        rect[3] -= rect[1]
        return rect

def save_cards():
    '''updates the None cards in the deck with the current cards if there remains unknown cards'''
    win_rec = _get_window_rect()
    margen = 6
    FIRST_CARD_REG = [142 + win_rec[0] + margen, 937 + win_rec[1] + margen, 95-2*margen, 90-2*margen]
    SPACE_BETWEEN_CARDS = 113
    CARDS = os.listdir('Cards1080p')
    for p in range(4):
        card_reg = FIRST_CARD_REG.copy()
        card_reg[0] = FIRST_CARD_REG[0] + p*SPACE_BETWEEN_CARDS
        im = pg.screenshot(region=card_reg)  # card region
        save_card = True
        # for card in CARDS:
        #     if pg.locate('Cards1080p/' + card, im, grayscale=True, confidence=.75) is not None:
        #         save_card = False
        #         break
        if save_card:
            pg.screenshot(f'C:/Users/joels/python-programs/GitHub/ClashRoyaleBot/Cards1080p/{random.randint(100000, 999999)}.png', region=card_reg)  # card region



def main():
    correct_window()
    while True:
        keyboard.wait('a')
        save_cards()


if __name__ == '__main__':
    main()
