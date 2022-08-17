# Information for how to play each card of the deck
from gameBoard import *

def f1(c: Card, game: GameBoard):
    if game.get_elixir() > 8:
        return 300
    return 100

def f2(c: Card, game: GameBoard):
    return (1000,1000)

BarbarianHut = Card('Barbarian Hut', f1, f2)
ElixirCollector = Card('Elixir Collector', f1, f2)
Furnace = Card('Furnace', f1, f2)
GoblinHut = Card('Goblin Hut', f1, f2)
IceWizard = Card('Ice Wizard', f1, f2)
Knight = Card('Knight', f1, f2)
Musketeer = Card('Musketeer', f1, f2)
Tombstone = Card('Tombstone', f1, f2)
FireSpirit = Card('Fire Spirit', f1, f2)
Bomber = Card('Bomber', f1, f2)
MegaMinion = Card('Mega Minion', f1, f2)

#for each card name associates its card class
CARDS_DICT = {
    'BarbarianHut' : BarbarianHut,
    'ElixirCollector' : ElixirCollector,
    'Furnace' : Furnace,
    'GoblinHut' : GoblinHut,
    'IceWizard' : IceWizard,
    'Knight' : Knight,
    'Musketeer' : Musketeer,
    'Tombstone' : Tombstone,
    'FireSpirit' : FireSpirit,
    'Bomber' : Bomber,
    'MegaMinion' : MegaMinion
}