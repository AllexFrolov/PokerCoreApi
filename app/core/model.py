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


def get_opp_hands(opp_range: float) -> list:
    opp_hands = []
    for g_hand, hand_stats in hands_range.items():
        if hand_stats['range'] < opp_range:
            opp_hands += group_hands[g_hand]
    return opp_hands

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
        response['expectation'] = pot
        return response
    
    hero_stats = players_stats[PlayerTypes.HERO.value]
    

    common_stack = 9999
    min_stack = 9999
    is_all_in = False
    for pl_name in action_sequence:
        player = players_stats[pl_name]
        common_stack = min(common_stack, player['stack'] + player['bet'])
        min_stack = min(min_stack, player['stack'])
        is_all_in |= player['all_in']

    
    if hero_stats['dealer'] | is_all_in:
        if min_stack < 3:
            opp_range = 1.
        elif min_stack < 5:
            opp_range = 0.9
        elif min_stack < 6:
            opp_range = 0.7
        elif min_stack < 10:
            opp_range = 0.5
        else:
            opp_range = 0.4
    else:
        opp_range = 0.6

    if is_all_in:
        fold_eq = 0
    else:
        fold_eq = (1 - opp_range) * pot


    
    opp_hands = get_opp_hands(opp_range)

    wr = hero_vs_range(hand, opp_hands, [], 1000)
    
    response['win_rate'] = wr

    expect = fold_eq + common_stack * (2*wr - 1)

    response['expectation'] = expect

    if expect > 0:
        response['action'] = Actions.ALL_IN.value
        response['bet_size'] = players_stats[PlayerTypes.HERO.value]['stack']
    else:
        response['action'] = Actions.FOLD.value
        response['bet_size'] = 0.
    
        
    return response


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
            pot=pot,
            positions=positions,
            action_sequence=action_sequence,
            players_stats=players_stats
            )

    else:
        opp_range = .8
        opp_hands = get_opp_hands(opp_range)

        wr = hero_vs_range(hand, opp_hands, board, 1000)
        response['win_rate'] = wr
        response['expectation'] = 0

        if wr > 0.5:
            response['action'] = Actions.ALL_IN.value
            response['bet_size'] = 0.
        else:
            response['action'] = Actions.FOLD.value
            response['bet_size'] = 0

    return response
