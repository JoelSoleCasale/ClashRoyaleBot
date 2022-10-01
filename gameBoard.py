from typing import Callable, List, Optional, Tuple, Type
import pyautogui as pg
import keyboard
import threading
import win32gui
import json
import time
import os

Pos = Tuple[int, int]
TimeStamp = float

CARDS_STATS = json.load(open('CardStats/useful_cards_stats.json'))

# Class definitions


class GameBoard:
    ...


class Card:
    ...


class Card:
    '''A card class that contains all the information for each card'''
    stats: dict  # all the card stats

    # a custom score for each card to determine how good would be to play that card with a ceratain GameBoard
    _score_func: Callable[[GameBoard], int]
    # returns the best place to place that card in a certain GameBoard
    _place_func: Callable[[GameBoard], Pos]

    def __init__(self, card_name: str, score_func1: Callable[[Card, GameBoard], int], place_func1: Callable[[GameBoard], Optional[Pos]]) -> None:
        self.stats = CARDS_STATS.get(card_name)
        assert self.stats is not None, f'the card with name: {card_name} has not been found'
        self._check_stats()

        self._score_func = score_func1
        self._place_func = place_func1

    def show_stats(self):
        print('-'*30)
        print(f"==============Name: {self.stats['name']}==============")
        for stat, value in self.stats.items():
            print(f"{stat}: {value}")

    def _check_stats(self):
        '''checks if all the required stats exists'''
        REQ_STATS = ["elixir"]
        for stat in REQ_STATS:
            assert self.stats.get(
                stat) is not None, f"missing {stat} stat in {self.stats['key']}"

    def score(self, game: GameBoard) -> int:
        '''returns an arbitary score about how good is to play this card in a certain gameboard'''
        return self._score_func(self, game)

    def place_in_board(self, game: GameBoard) -> Optional[Pos]:
        '''returns the best position to place this card in a certain gameboard.
        returns None if the card cant be placed'''
        return self._place_func(self, game)


class GameBoard:
    '''A class that contains all the information avaliable about the current state of the game board
    during a match. Controls all the actions and information inside a match'''

    _LEVELS: List[str]  # a list of all the levels images to ckeck

    deck_cards: List[Optional[str]]  # actual cards in deck
    _known_cards: int  # the known cards from the deck
    next_cards: List[Optional[str]]  # next cards to come

    _elixir: int  # acutal elixir

    _game_start_time: float  # the instant the game started
    _game_multiplier: float  # game elixir multiplier

    # a list with all the enemy positions in the board
    _enemy_positions: List[Pos]
    # a log with each card that has been used the moment, where and when
    _used_cards: List[Tuple[TimeStamp, str, Pos]]

    def __init__(self):
        self.deck_cards = [None for i in range(4)]
        self._known_cards = 0
        self.next_cards = [None for i in range(4)]
        self._elixir = 0

        self._game_multiplier = 1
        self._game_start_time = time.time()
        self._used_cards = []

        self._LEVELS = ['EnemyLevels1080p/' +
                        x for x in os.listdir('EnemyLevels1080p') if x[-4:] == '.png']

    def update_elixir(self) -> int:
        '''updates the current elixir in game and returns it'''
        win_rec = self._get_window_rect()
        FIRST_PIXEL = (202+win_rec[0], 1081+win_rec[1])  # first pixel to check
        ELIXIR_SPACE_BETWEEN = 42  # space between pixels to check
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
        # if self._known_cards == 8:
        #     return None
        # para tener en cuenta la posición inicial de la ventana
        win_rec = self._get_window_rect()
        FIRST_CARD_REG = [142 + win_rec[0], 930 + win_rec[1], 95, 90]
        SPACE_BETWEEN_CARDS = 113
        CARDS = os.listdir('Cards1080p')
        for p in range(4):
            if self.deck_cards[p] is None:
                card_reg = FIRST_CARD_REG.copy()
                card_reg[0] = FIRST_CARD_REG[0] + p*SPACE_BETWEEN_CARDS
                im = pg.screenshot(region=card_reg)  # card region
                for card in CARDS:
                    if pg.locate('Cards1080p/' + card, im, grayscale=True, confidence=.75) is not None:
                        # to remove the final ".png"
                        self.deck_cards[p] = card[:-4]
                        self._known_cards += 1
                        break

    def show_deck(self):
        '''shows the current state of the deck and the next cards to come in terminal'''
        print(f"Deck cards: {[card.name if card is not None else 'None' for card in self.deck_cards ]}")
        print(f"Next cards: {[card.name if card is not None else 'None' for card in self.next_cards ]}")

    def update_enemies(self, reg=(47, 142, 515, 704)) -> None:
        '''updates all the enemy positions in a certain region,
        by default the region is all the screen'''
        win_rec = self._get_window_rect()
        pos = []
        im1 = pg.screenshot(
            region=(reg[0]+win_rec[0], reg[1]+win_rec[1], reg[2], reg[3]))  # game region
        for level in self._LEVELS:
            for x in list(pg.locateAll(level, im1, grayscale=True, confidence=.8)):
                x1 = (x[0]+reg[0], x[1]+reg[1])
                add = True
                for x0 in pos:
                    if (x0[0] - 15 <= x1[0] <= x0[0] + 15) and (x0[1] - 15 <= x1[1] <= x0[1] + 15):
                        add = False  # to avoid detecting twice the same enemy
                        break
                if add:
                    p = pg.pixel(int(x1[0]) + 5+win_rec[0],
                                 int(x1[1]) + 13+win_rec[1])
                    if p[0] > 80 and p[2] < 80:  # check if the card corresponds to an enemy one
                        pos.append(x1)
        self._enemy_positions = pos

    def enemies_pos(self) -> List[Pos]:
        '''returns a list of all the enemy positions in screen, must be updated with the "update_enemy_pos" function'''
        return self._enemy_positions

    def enemies_in_reg(self, reg: List[int]) -> int:
        '''returns the number on enemies in a certain region of the map'''
        tot = 0
        for enemy in self.enemies_pos():
            if reg[0] <= enemy[0] <= reg[0]+reg[2] and reg[1] <= enemy[1] <= reg[1]+reg[3]:
                tot += 1
        return tot

    def update_card(self, index: int, card: str):
        self.deck_cards[index] = card

    def place_card(self, card: str, pos: Pos) -> None:
        '''places a card from the deck in a certain position on the board'''
        index = self.deck_cards.index(card)
        assert 0 <= index < 4
        win_rec = self._get_window_rect()
        pg.press(str(index+1))
        pg.moveTo(pos[0]+win_rec[0], pos[1]+win_rec[1], duration=.1)
        pg.click()
        self._used_cards.append((self.passed_time(), card, pos))
        # we update the deck:
        self.deck_cards[index] = None
        # time.sleep(.5)
        # threading.Timer(2, self.update_card, [index, self.next_cards[0]]).start()
        self.next_cards.pop(0)
        self.next_cards.append(card)

    def _get_window_rect(name="BlueStacks App Player") -> List[int]:
        '''returns a list with the coordinates and dimensions, returns [x, y, w, h]'''
        rect = list(win32gui.GetWindowRect(
            win32gui.FindWindow(None, "BlueStacks App Player")))
        rect[2] -= rect[0]
        rect[3] -= rect[1]
        return rect

    def game_ended(self) -> bool:
        '''returns if the game has ended or not'''
        # checks 8 pixels and their color to determine if the game has ended
        if self.passed_time() > 300:
            return True
        win_rec = self._get_window_rect()
        check_pos = [[(70, 615), (36, 94, 172)], [(69, 664), (39, 100, 185)], [(545, 611), (24, 67, 120)], [(545, 665), (27, 78, 144)], [
            (68, 313), (153, 12, 64)], [(69, 360), (158, 12, 64)], [(530, 317), (107, 8, 44)], [(530, 360), (120, 10, 52)]]
        for pos in check_pos:
            if not pg.pixelMatchesColor(pos[0][0]+win_rec[0], pos[0][1]+win_rec[1]+12, pos[1], 20):
                return False
        return True

    def get_crowns(enemy: bool) -> int:
        '''returns the enemy or ally crowns, True for enemy, False for ally
        prec: the game must have ended'''
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
