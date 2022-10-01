''' 
Main script that manages the games
'''
from typing import List
import pyautogui as pg
import time
from datetime import datetime
from CRCards2 import *


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


def get_window_rect(name="BlueStacks App Player") -> List[int]:
        '''returns a list with the coordinates and dimensions, returns [x, y, w, h]'''
        rect = list(win32gui.GetWindowRect(win32gui.FindWindow(None, "BlueStacks App Player")))
        rect[2] -= rect[0]
        rect[3] -= rect[1]
        return rect


def move_and_click(pos: Pos, t: float):
    '''moves the mouse in a certain position of the game window and clicks it, then waits t time'''
    win_rec = get_window_rect()
    pg.moveTo(pos[0]+win_rec[0], pos[1]+win_rec[1])
    pg.click()
    time.sleep(t)


def start_game(gamemode: str = 'showdown') -> None:
    '''starts a game in a certain gamemode, can be: showdown, special, practice, or normal'''
    clicks: List[Pos]
    if gamemode == 'showdown':
        clicks = [(429, 737), (434, 794), (307, 734)]
    elif gamemode == 'special':
        clicks = [(403, 738), (440, 519), (307, 734)]
    elif gamemode == 'practice':
        clicks = [(556, 149), (375, 386), (413, 657)]
    elif gamemode == 'normal':
        clicks = [(180, 745), (307, 734)]
    assert clicks, 'Invalid gamemode'
    for click in clicks:
        move_and_click(click, .15)


def exit_game():
    move_and_click((304, 958), 4)


def check_maestry_rewards():
    '''check if there is any maestry rewards and claims it if necesary'''
    win_rec = get_window_rect()
    if pg.pixel(191+win_rec[0], 1085+win_rec[1])[0] > 200:
        seq = [(158, 1048), (551, 823), (122, 341), (316, 811), (316, 811), (328, 662), (328, 662), (332, 776), (332, 776), (342, 618), (342, 618), (342, 698), (342, 698), (364, 606), (364, 606), (363, 718), (363, 718), (368, 587), (363, 724), (361, 576), (367, 721), (363, 591), (358, 723), (370, 589), (365, 738), (355, 594),
        (549, 181), (542, 216), (353, 1059)]
        for action in seq:
            move_and_click(action, .3)


def strat_2():
    UNKNOWN_SCORE = 100 # the score of an unknown card
    MINIMUM_SCORE = 200 # minimum score to place a card

    game = GameBoard()
    while game.update_elixir() < 7 and not game.game_ended():
        time.sleep(.1)
    # The game started
    t1 = time.time()
    while not game.game_ended():
        game.update_deck()
        game.update_enemies()
        game.update_elixir()
        card_scores = [UNKNOWN_SCORE for i in range(4)]
        print(str(game.deck_cards)+' '*30, end='\r')
        for i in range(4):
            if game.deck_cards[i] is not None:
                card_scores[i] = CARDS_DICT[game.deck_cards[i]].score(game)
        
        max_index = card_scores.index(max(card_scores))
        card_to_play = game.deck_cards[max_index] if max(card_scores) > MINIMUM_SCORE else None
        if card_to_play is not None:
            pos = CARDS_DICT[game.deck_cards[max_index]].place_in_board(game)
            if pos is not None:
                game.place_card(game.deck_cards[max_index], pos)
        # print(f"Iteration time: {time.time()-t1}", end='\r')
        t1 = time.time()

def correct_window():
    '''The BlueStacks window must be fullHD, and with the correct with and height'''
    hwnd = win32gui.FindWindow(None, "BlueStacks App Player")
    rect = list(win32gui.GetWindowRect(hwnd))
    win32gui.MoveWindow(hwnd, rect[0], rect[1], 637, 1108, True)

def main():
    for i in range(10**4): # number of games to play
        correct_window()
        print(f'{datetime.now().strftime("%H:%M:%S")} | Game {i+1}'+' '*60)
        start_game('special')
        strat_2()
        time.sleep(1)
        exit_game()
        check_maestry_rewards()


if __name__ == '__main__':
    main()