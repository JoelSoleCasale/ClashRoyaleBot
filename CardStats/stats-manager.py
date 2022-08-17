import json

def generate_useful_info() -> dict():
    '''picks the useful information about each card from the cards_stats.json and cards.json files
    and generates a new json file'''
    CARDS_STATS = json.load(open('CardStats/cards_stats.json'))
    CARDS_BASICS = json.load(open('CardStats/cards.json'))
    card_names = [card['name'] for card in CARDS_BASICS]
    cards_dict = {card:dict() for card in card_names}

    # Basic information
    for i, card in enumerate(card_names):
        d = CARDS_BASICS[i]
        info = {x:d.get(x) for x in ["key", "elixir", "type"] if d.get(x) is not None}
        cards_dict[card] = info
        assert info.get("elixir") is not None and info.get("type") is not None
    
    # Advanced information
    USEFUL_INFO = ["name", "life_time", "deploy_time", "speed", "hitpoints", "range", "attacks_air", "target_only_buildings", "pve_defense_type", "spawn_character", "summon_character", "summon_number", "damage", "radius", "buff"]
    for name, card in cards_dict.items():
        category = card['type'].lower()
        if name == "Heal Spirit": #an exception
            category = "spell"
        names = [c.get('name_en') for c in CARDS_STATS[category]]
        if name in names:
            d = CARDS_STATS[category][names.index(name)]
            info = {x:d[x] for x in USEFUL_INFO if d.get(x) is not None}
            card |= info #we merge both dictionaries
    
    # Get information about the summoned characters
    char_names = [c.get('name') for c in CARDS_STATS['characters']]
    for name, card in cards_dict.items():
        if card['type'] == 'Troop':
            summon_char_name = card['summon_character']
            character = CARDS_STATS['characters'][char_names.index(summon_char_name)]
            info = {x:character[x] for x in USEFUL_INFO if character.get(x) is not None}
            card |= info
    
    # Get information about spells with their projectiles
    proj_names = [c.get('name') for c in CARDS_STATS['projectile']]
    for name, card in cards_dict.items():
        if card['type'] == 'Spell':
            proj_name = name.replace(" ", "") + "Spell"
            if proj_name in proj_names:
                proj = CARDS_STATS['projectile'][proj_names.index(proj_name)]
                info = {x:proj[x] for x in USEFUL_INFO if proj.get(x) is not None}
                card |= info

    return cards_dict

def main():
    info = generate_useful_info()
    with open('CardStats/useful_cards_stats.json', 'w') as ucs:
        json.dump(info, ucs, sort_keys=True, indent=4)

if __name__ == '__main__':
    main()