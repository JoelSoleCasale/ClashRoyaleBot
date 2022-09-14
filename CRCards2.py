# Information for how to play each card of the deck
from gameBoard import *
import random


def f1(c: Card, game: GameBoard):
    if game.get_elixir() >= 8:
        return random.randint(200, 300)
    if game.get_elixir()+1 >= c.stats.get('elixir', 9):
        return random.randint(200, 300)
    return 100


def f2(c: Card, game: GameBoard):
    avX = sum([x for x, y in game.enemies_pos()])//len(game.enemies_pos()) if game.enemies_pos() else random.randint(52, 558)
    avY = sum([y for x, y in game.enemies_pos()])//len(game.enemies_pos()) if game.enemies_pos() else random.randint(52, 558)
    if c.stats.get('hitpoints', 10) > 1000:  # tank unit
        return (avX, 635)
    if c.stats.get('type', '') == 'Spell':
        if game.enemies_pos():
            return (avX, avY + 180)
        return (144, 262)  # atacar a la torre
    if c.stats.get('type', '') == "Building":
        if c.stats.get('range', 0) >= 11000:
            return (random.randint(100, 500), 535)
        return (random.randint(280, 320), 680)
    return (avX, random.randint(680, 823))


# BarbarianHut = Card('Barbarian Hut', f1, f2)
# ElixirCollector = Card('Elixir Collector', f1, f2)
# Furnace = Card('Furnace', f1, f2)
# GoblinHut = Card('Goblin Hut', f1, f2)
# IceWizard = Card('Ice Wizard', f1, f2)
# Knight = Card('Knight', f1, f2)
# Musketeer = Card('Musketeer', f1, f2)
# Tombstone = Card('Tombstone', f1, f2)
# FireSpirit = Card('Fire Spirit', f1, f2)
# Bomber = Card('Bomber', f1, f2)
# MegaMinion = Card('Mega Minion', f1, f2)
# IceSpirit = Card('Ice Spirit', f1, f2)
# MiniPEKKA = Card('Mini P.E.K.K.A', f1, f2)

# for each card name associates its card class
CARDS_DICT = {
    # 'BarbarianHut': BarbarianHut,
    # 'ElixirCollector': ElixirCollector,
    # 'Furnace': Furnace,
    # 'GoblinHut': GoblinHut,
    # 'IceWizard': IceWizard,
    # 'Knight': Knight,
    # 'Musketeer': Musketeer,
    # 'Tombstone': Tombstone,
    # 'FireSpirit': FireSpirit,
    # 'Bomber': Bomber,
    # 'MegaMinion': MegaMinion,
    # 'IceSpirit': IceSpirit,
    # 'MiniPEKKA': MiniPEKKA
}

# for any card not defined in the dict set the default value:
names = [name for name, card in CARDS_STATS.items()]
for name in names:
    if not name.replace(' ', '').replace('.', '') in CARDS_DICT.keys():
        CARDS_DICT[name.replace(' ', '').replace('.', '')] = Card(name, f1, f2)

if __name__ == '__main__':
    a = sorted([name for name, card in CARDS_DICT.items()])
    print(a)
