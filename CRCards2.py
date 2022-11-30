'''
Script that manages all the information about the cards and how to play it
'''
from gameBoard import *
import random


def f1(c: Card, game: GameBoard) -> int:
    '''Given a card c and a GameBoard state,
    returns an arbitrary number depending on how good it would be to play that card'''
    if c.stats.get('type','') == 'Spell' and not game.enemy_pos():
        return 0
    if 'Tornado' in game.deck_cards and 'Rocket' in game.deck_cards:
        if c.stats.get('name', '') == 'Tornado' and game.get_elixir() >=7:
            return 1000
        return 0
    if game._used_cards and game._used_cards[-1][1] == 'Tornado':
        if 'Rocket' in game.deck_cards:
            if c.stats.get('name', '') == 'RocketSpell':
                return 1000
            return 0
    if game.get_elixir() >= 8:
        return random.randint(200, 300)
    if game.get_elixir()+1 >= c.stats.get('elixir', 9):
        return random.randint(100, 300)
    return 100


def f2(c: Card, game: GameBoard) -> Pos:
    '''Given a card to place c and a GameBoard state,
    returns the best position to place that card in the board'''
    avX = sum([x for x, y in game.enemy_pos()])//len(game.enemy_pos()) if game.enemy_pos() else random.randint(52, 558)
    avY = sum([y for x, y in game.enemy_pos()])//len(game.enemy_pos()) if game.enemy_pos() else random.randint(52, 558)
    if c.stats.get('hitpoints', 10) > 1000:  # tank unit
        return (avX, 635)
    if c.stats.get('type', '') == 'Spell':
        if game._used_cards and game._used_cards[-1][1] == 'Tornado':
            return (game._used_cards[-1][2][0], game._used_cards[-1][2][1] + 10)
        if game.enemy_pos():
            return (avX, avY + 180)
        return (144, 262)  
    if c.stats.get('type', '') == "Building":
        if c.stats.get('range', 0) >= 11000:
            return (random.randint(100, 500), 535)
        return (random.randint(280, 320), 680)
    return (avX, random.randint(680, 823))

# for each card name associates its card class
CARDS_DICT = { }

# for any card not defined in the dict set the default value:
names = [name for name, card in CARDS_STATS.items()]
for name in names:
    if not name.replace(' ', '').replace('.', '') in CARDS_DICT.keys():
        CARDS_DICT[name.replace(' ', '').replace('.', '')] = Card(name, f1, f2)

if __name__ == '__main__':
    print(sorted([name for name, card in CARDS_DICT.items()]))
