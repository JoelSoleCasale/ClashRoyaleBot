# Information for how to play each card of the deck
from gameBoard import *

CARDS_STATS = json.load(open('useful_cards_stats.json'))

class Card:
    stats: dict # all the card stats

    def __init__(self, card_name: str) -> None:
        self.stats = CARDS_STATS.get(card_name)
        assert self.stats is not None, f'the card with name: {card_name} has not been found'
        self._check_stats()
    
    def show_stats(self):
        print(f"Name: {self.stats['name']}\n")
        for stat, value in self.stats.items():
            print(f"{stat}: {value}")
    
    def _check_stats(self):
        '''checks if all the required stats exists'''
        REQ_STATS = ["name", "elixir"]
        for stat in REQ_STATS:
            assert self.stats[stat] is not None, f"missing {stat} stat in {self.stats['key']}"


BarbarianHut = Card('Barbarian Hut')
ElixirCollector = Card('Elixir Collector')
Furnace = Card('Furnace')
GoblinHut = Card('Goblin Hut')
IceWizard = Card('Ice Wizard')
Knight = Card('Knight')
Musketeer = Card('Musketeer')
Tombstone = Card('Tombstone')
FireSpirit = Card('Fire Spirit')
Bomber = Card('Bomber')
MegaMinion = Card('Mega Minion')

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