from argparse import ONE_OR_MORE
from typing import List, Optional
from typing_extensions import TypeAlias
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

class GameBoard:
    '''A class that contains all the information avaliable about the current state of the game board
    during a match'''

    _LEVELS: List[str] # a list of all the levels images to ckeck

    deck_cards: List[Optional[Card]] # actual cards in deck
    _known_cards: int # the known cards from the deck
    next_cards: List[Optional[Card]] # next cards to come

    _elixir: int # acutal elixir

    _game_start_time: float # the instant the game started
    _game_multiplier: float # game elixir multiplier

    _enemy_positions: List[Pos] # a list with all the enemy positions in the board
    _used_cards: List[Tuple[TimeStamp, Card, Pos]] # a log with each card that has been used the moment, where and when

    def __init__(self):
        self.deck_cards = [None for i in range(4)]
        self._known_cards = 0
        self.next_cards = [None for i in range(4)]
        self._elixir = 0

        self._game_multiplier = 1
        self._game_start_time = time.time()

        self._LEVELS = ['EnemyLevels/' + x for x in os.listdir('EnemyLevels') if x[-4:] == '.png']

    def update_elixir(self) -> int:
        '''updates the current elixir in game and returns it'''
        FIRST_PIXEL = (1135, 1370) # first pixel to check
        ELIXIR_SPACE_BETWEEN = 50 # space between pixels to check
        for i in range(10):
            if pg.pixel(FIRST_PIXEL[0]+i*ELIXIR_SPACE_BETWEEN, FIRST_PIXEL[1])[0] < 150:
                self._elixir = i
                return i
        self._elixir = 10
        return 10

    def get_elixir(self) -> int:
        '''returns the current elixir in game, must be updated with the "update_elixir" function'''
        return self._elixir

    def passed_time(self) -> float:
        '''returns the time that passed since the game began'''
        return time.time() - self._game_start_time

    def update_deck(self) -> None:
        '''updates the None cards in the deck with the current cards if there remains unknown cards'''
        if self._known_cards == 8:
            return None
        FIRST_CARD_REG = [1060, 1175, 120, 130]
        SPACE_BETWEEN_CARDS = 145
        CARDS = os.listdir('Cards')
        for p in range(4):
            if self.deck_cards[p] is None:
                card_reg = FIRST_CARD_REG
                card_reg[0] = FIRST_CARD_REG[0] + p*SPACE_BETWEEN_CARDS
                im = pg.screenshot(region=card_reg) #card region
                for card in CARDS:
                    if pg.locate('Cards/' + card, im, grayscale=True, confidence=.93) is not None:
                        self.deck_cards[p] = CARDS_DICT[card[:-4]] # to remove the final ".png"
                        self._known_cards += 1
                        break

    def show_deck(self):
        '''shows the current state of the deck and the next cards to come in terminal'''
        print(f"Deck cards: {[card.name if card is not None else 'None' for card in self.deck_cards ]}")
        print(f"Next cards: {[card.name if card is not None else 'None' for card in self.next_cards ]}")

    def update_enemy_pos(self, reg=(930, 160, 670, 915)) -> None:
        '''updates all the enemy positions in a certain region,
        by default the region is all the screen'''
        pos = []
        im1 = pg.screenshot(region=reg) #game region
        for level in self._LEVELS:
            for x in list(pg.locateAll(level, im1, confidence=.95)):
                x1 = (x[0]+reg[0], x[1]+reg[1])
                if pos:
                    x0 = pos[-1]
                    if not(x0[0]<= x1[0] <= x0[0] + 15) and not(x0[1]<= x1[1] <= x0[1] + 15):
                        pos.append(x1)
                else:
                    pos.append(x1)
        self._enemy_positions = pos

    def enemy_pos(self) -> List[Pos]:
        '''returns a list of all the enemy positions in screen,
        must be updated with the "update_enemy_pos" function'''
        return self._enemy_positions

    def place_card(self, card: Card, pos: Pos) -> None: 
        '''places a card from the deck in a certain position on the board'''
        index = self.deck_cards.index(card)
        assert 0 <= index < 4 
        pg.press(str(index+1))
        pg.moveTo(pos, duration=.1)
        pg.click()
        self._used_cards.append((self.passed_time(), card, pos))
        # we update the deck:
        self.deck_cards[index] = self.next_cards[0]
        self.next_cards.pop(0)
        self.next_cards.append(card)

    def game_ended(self) -> bool:
        '''returns if the game has ended or not'''
        END_GAME_REG = (917, 656, 687, 285)
        im = pg.screenshot(region=END_GAME_REG)
        return pg.locate("end-game1.png", im, confidence=.9) is not None or keyboard.is_pressed('ç')

def get_crowns(enemy: bool) -> int:
    '''returns the enemy or ally crowns, True for enemy, False for ally'''
    if enemy:
        pixels = [(1082, 341), (1260, 325), (1437, 342)]
        for i in range(3):
            if pg.pixel(pixels[i][0], pixels[i][1])[1] < 120:
                return i
        return 3
    else:
        pixels = [(1085, 743), (1263, 724), (1441, 744)]
        for i in range(3):
            if pg.pixel(pixels[i][0], pixels[i][1])[0] < 200:
                return i
        return 3

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
    enemies = game.enemy_pos()
    print(enemies)
    for enemy in enemies:
        pg.moveTo(enemy)
        time.sleep(1)

if __name__ == '__main__':
    test()