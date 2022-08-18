from typing import List, Optional
import pyautogui as pg
import random
import keyboard
import time
import os
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
    assert clicks
    for click in clicks:
        move_and_click(click, .15)

def exit_game():
    move_and_click((304, 958), 4)

def check_maestry_rewards():
    if pg.pixel(1070, 1390)[0] > 200:
        seq = [(1070, 1390), (1587, 1039), (1031, 435), (1274, 734), (1264, 919), (1269, 735), (1293, 908), (1285, 728), (1273, 912), (1250, 727), (1249, 911), (1240, 725), (1253, 883), (1253, 740), (1276, 914), (1575, 224), (1566, 267), (1329, 1335)]
        for action in seq:
            pg.moveTo(action, duration=.3)
            pg.click()

def strat_2():
    UNKNOWN_SCORE = 100 # the score of an unknown card
    MINIMUM_SCORE = 200 # minimum score to place a card

    game = GameBoard()
    while game.update_elixir() < 7:
        time.sleep(.1)
    # The game started
    t1 = time.time()
    while not game.game_ended():
        game.update_deck()
        game.update_enemies()
        game.update_elixir()
        card_scores = [UNKNOWN_SCORE for i in range(4)]
        for i in range(4):
            if game.deck_cards[i] is not None:
                card_scores[i] = CARDS_DICT[game.deck_cards[i]].score(game)
        
        print(card_scores)
        max_index = card_scores.index(max(card_scores))
        card_to_play = game.deck_cards[max_index] if max(card_scores) > MINIMUM_SCORE else None
        if card_to_play is not None:
            pos = CARDS_DICT[game.deck_cards[max_index]].place_in_board(game)
            if pos is not None:
                game.place_card(game.deck_cards[max_index], pos)
        print(f"Iteration time: {time.time()-t1}")
        t1 = time.time()

def main():
    wins, loses, total_crowns = 0, 0, 0
    t_end = time.time() + 3600
    for i in range(1):
        start_game('practice')
        strat_2()
        exit_game()

def wait_for_key(k):
    '''waits until the key k is pressed, used for debugging'''
    while(keyboard.is_pressed(k) is False):
        time.sleep(.05)
    while(keyboard.is_pressed(k) is True):
        time.sleep(.05)

@timing
def enemy_pos_test():
    game = GameBoard()
    while(True):
        wait_for_key('a')
        game.update_enemies()
        enemies = game.enemies_pos()
        print(enemies)
        for e in enemies:
            pg.moveTo((int(e[0]), int(e[1])))
            print(pg.pixel(int(e[0])+5, int(e[1])+13))
            time.sleep(.5)

if __name__ == '__main__':
    enemy_pos_test()