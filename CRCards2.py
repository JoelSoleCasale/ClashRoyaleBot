# Information for how to play each card of the deck
from dataclasses import dataclass
from typing import Optional, Tuple, List
import json

Pos = Tuple[int, int]

CARDS_STATS = json.load(open('cards_stats.json'))
CARDS_BASICS = json.load(open('cards.json'))
for card in CARDS_BASICS['ElectroWizard']:
    print(card)

def info(card: str, useful_info: List[str]) -> dict:
    '''returns the required useful info about a given card in form of a dictionary'''
    # categories to search in
    categories = ['building', 'spell', 'projectile', 'characters']

    for category in categories:
        names = [card['name'] for card in CARDS_STATS[category]]
        if card in names:
            d = CARDS_STATS[category][names.index(card)]
            info = {x:d.get(x, None) for x in useful_info}
            card_info = info
            card_info['elixir'] = CARDS_BASICS[card]['elixir']
            card_info['type'] = category
            del card_info['mana_cost']
            return card_info

class Card:
    stats: dict # all the card stats
    USEFUL_INFO = ["name", "life_time", "deploy_time", "speed", "hitpoints", "range", "attacks_ground", "attacks_air", "target_only_buildings"]

    def __init__(self, card_name: str) -> None:
        self.stats = info(card_name, self.USEFUL_INFO)
        assert self.stats is not None, f'the card with name: {card_name} has not been found'
        self._check_stats()
    
    def show_stats(self):
        for stat, value in self.stats.items():
            print(f"{stat}: {value}")
    
    def _check_stats(self):
        '''checks all the necesary stats are correct'''
        NEC_STATS = ["name", "elixir"]
        for stat in NEC_STATS:
            assert self.stats[stat] is not None, f"missing {stat} stat in {self.stats['name']}"

BarbarianHut = Card('BarbarianHut')
ElixirCollector = Card('ElixirCollector')
ElixirCollector.show_stats()
Furnace = Card('FirespiritHut')
GoblinHut = Card('GoblinHut')
IceWizard = Card('IceWizard')
Knight = Card('Knight')
Musketeer = Card('Musketeer')
Tombstone = Card('Tombstone')
FireSpirit = Card('FireSpirits')
Bomber = Card('Bomber')
MegaMinion = Card('MegaMinion')

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