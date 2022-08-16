# Information for how to play each card of the deck
from dataclasses import dataclass
from typing import Optional, Tuple, List, Union
from typing_extensions import TypeAlias
import json

Pos = Tuple[int, int]

@dataclass
class Card:
    name: str
    elixir: int
    area: bool # if it's attack is on area
    structure: bool # if it's a structure or a card
    lifetime: Optional[int] # structure lifetime
    stats_info: dict

BarbarianHut = Card('BarbarianHut', 7, False, True, 40)
ElixirCollector = Card('ElixirCollector', 6, False, True, 65)
Furnace = Card('Furnace', 4, False, True, 33)
GoblinHut = Card('GoblinHut', 5, False, True, 31)
IceWizard = Card('IceWizard', 3, True, False, None, {'deploy_time': 1000, 'speed': 60, 'hitpoints': 569, 'range': 5500, 'attacks_ground': True, 'attacks_air': True, 'target_only_buildings': False, 'type': 'troop'})
Knight = Card('Knight', 3, False, False, None, {'deploy_time': 1000, 'speed': 60, 'hitpoints': 651, 'range': 1200, 'attacks_ground': True, 'attacks_air': False, 'target_only_buildings': False, 'type': 'troop'})
Musketeer = Card('Musketeer', 4, False, False, None, {'deploy_time': 1000, 'speed': 60, 'hitpoints': 340, 'range': 6000, 'attacks_ground': True, 'attacks_air': True, 'target_only_buildings': False, 'type': 'troop'})
Tombstone = Card('Tombstone', 3, False, True, 30)
FireSpirit = Card('FireSpirit', 1, True, False, None)
Bomber = Card('Bomber', 2, True, False, None, {'deploy_time': 1000, 'speed': 60, 'hitpoints': 130, 'range': 4500, 'attacks_ground': True, 'attacks_air': False, 'target_only_buildings': False, 'type': 'troop'})
MegaMinion = Card('MegaMinion', 3, False, False, None, {'deploy_time': 1000, 'speed': 60, 'hitpoints': 395, 'range': 1600, 'attacks_ground': True, 'attacks_air': True, 'target_only_buildings': False, 'type': 'troop'})

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


# Opening JSON file
with open('cards_stats.json') as json_file:
    data = json.load(json_file)
    
    useful_information = ["deploy_time", "speed", "hitpoints", "range", "attacks_ground", "attacks_air", "target_only_buildings"] #, "elixir", "type"
    # Print the type of data variable
    print("Type:", type(data))
    print(len(data["characters"]))
    names = [troop['name'] for troop in data["characters"]]
    cards = [card for card in CARDS_DICT]
    cards_info = {}
    for card in cards:
        if card in names:
            d = data["characters"][names.index(card)]
            info = {x:d.get(x, None) for x in useful_information}
            cards_info[card] = info
    print(cards_info)