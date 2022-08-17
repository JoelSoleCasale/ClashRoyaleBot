from typing import List, Optional
import pyautogui as pg
import random
import keyboard
import time
import os
from CRCards2 import *

#=======REGIONS=======#
SCREEN_REG = (930, 160, 670, 915)
L_REG = (930, 160, 335, 915)
R_REG = (1265, 160, 335, 915)
LOW_L_REG = (937, 467, 328, 582)
LOW_R_REG = (1263, 466, 327, 593)

TimeStamp = float

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

def start_game(gamemode: str = 'showdown') -> None:
    '''starts a game in a certain gamemode, can be: showdown, special, practice, or normal'''
    clicks: List[Pos]
    if gamemode == 'showdown':
        clicks = [(1419, 939), (1445, 1008), (1262, 895)]
    elif gamemode == 'special':
        clicks = [(1415, 934), (1446, 650), (1262, 895)]
    elif gamemode == 'practice':
        clicks = [(1587, 180), (1347, 483), (1407, 818)]
    elif gamemode == 'normal':
        clicks = [(1123, 947), (1262, 895)]
    assert clicks
    for click in clicks:
        pg.moveTo(click, duration=.15)
        pg.click()

def exit_game():
    pg.moveTo(1270, 1200, .1)
    pg.click()
    time.sleep(4)

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
    while not game.game_ended():
        game.update_deck()
        game.update_enemy_pos()
        game.update_elixir()
        card_scores = [UNKNOWN_SCORE for i in range(4)]
        for i in range(4):
            if game.deck_cards[i] is not None:
                card_scores[i] 

def main():
    wins, loses, total_crowns = 0, 0, 0
    t_end = time.time() + 3600
    for i in range(1):
        start_game('practice')
        strat_2()
        exit_game()

def test():
    game = GameBoard()
    game.update_enemy_pos()
    enemies = game.enemy_pos()
    print(enemies)

if __name__ == '__main__':
    test()