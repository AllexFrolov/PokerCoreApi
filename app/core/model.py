#pylint: disable=missing-docstring
import json

from schemas import Actions, PlayerTypes, PokerStage

from .montecarlo import hero_vs_range



with open('./data/hands_range.json', 'r') as f:
    hands_range =  json.loads(f.read())

with open('./data/hands.json', 'r') as f:
    hands_combination = json.loads(f.read())

with open('./data/group_hands.json', 'r') as f:
    group_hands = json.loads(f.read())


def preflop(hand: list[str], 
            pot: float,
            positions: list[str],
            action_sequence: list[str],
            players_stats: dict
            ) -> dict:

    response = {
        'action': None,
        'win_rate': 0,
    }

    if len(action_sequence) == 1:
        response['action'] = Actions.RAISE.value
        response['win_rate'] = 1.0
        response['bet_size'] = 0.
        return response
    
    hero_stats = players_stats[PlayerTypes.HERO.value]

    if hero_stats['bet_size'] == 0:
        if hero_stats['is_dealer']:
            opp_range = 0.4
    
    

    opp_hands = []
    for g_hand, hand_stats in hands_range.items():
        if hand_stats['range'] < opp_range:
            opp_hands += group_hands[g_hand]

    wr = hero_vs_range(hand, opp_hands, [], 1000)
    
    response['win_rate'] = wr

    if wr >= 0.5:
        response['action'] = Actions.ALL_IN.value
        response['bet_size'] = players_stats[PlayerTypes.HERO.value]['stack']
    
        
    return {
    'action': Actions.FOLD,
    'amount': 0}


def make_action(
        hand: list[str],
        board: list[str],
        stage: str,
        pot: float,
        positions: list[str],
        action_sequence: list[str],
        players_stats: dict,
        *args, **kwargs) -> dict:

    response = {
        'action': None,
        'win_rate': 0,
    }
                
    if stage == PokerStage.PREFLOP.value:
        return preflop(
            hand=hand,
            board=board,
            pot=pot,
            positions=positions,
            action_sequence=action_sequence,
            players_stats=players_stats
            )

    else:
        response['action'] = Actions.FOLD.value
        response['bet_size'] = 0

    return response
