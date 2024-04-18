#pylint: disable=missing-docstring
import json

from schemas import Actions

from .montecarlo import hero_vs_range



with open('./data/hands_range.json', 'r') as f:
    hands_range =  json.loads(f.read())

with open('./data/hands.json', 'r') as f:
    hands_combination = json.loads(f.read())

with open('./data/group_hands.json', 'r') as f:
    group_hands = json.loads(f.read())


def make_action(hand: list[str], board: list[str], stage: str, pot: float, *args, **kwargs) -> dict:

    response = {
        'action': None,
        'win_rate': 0,
    }
    if stage == 'preflop':
        opp_range = 0.5
    else:
        opp_range = 0.4

    opp_hands = []
    for g_hand, hand_stats in hands_range.items():
        if hand_stats['range'] < opp_range:
            opp_hands += group_hands[g_hand]

    wr = hero_vs_range(hand, opp_hands, board, 1000)
    response['win_rate'] = wr

    if wr >= 0.5:
        response['action'] =  Actions.PUSH.value
    else:
        response['action'] =  Actions.FOLD.value

    return response
