#pylint: disable=missing-docstring
import json

from config.config import (
    DEFAULT_WR_CUM,
    )

from schemas import Actions

from .montecarlo import hero_vs_range



with open('./data/hands_range.json', 'r') as f:
    hands_range =  json.loads(f.read())

with open('./data/hands.json', 'r') as f:
    hands_combination = json.loads(f.read())


def make_action(hand: list[str], board: list[str], win_rate: float=None) -> dict:

    response = {
        'action': None,
        'win_rate': 0,
    }

    opp_range = [['7h', '7d'], ['7h', '7c'], ['7h', '7s'], ['7d', '7c'], ['7d', '7s'], ['7c', '7s']]

    wr = hero_vs_range(hand, opp_range, board, 10000)
    response['win_rate'] = wr

    if win_rate is None:
        win_rate = DEFAULT_WR_CUM

    if wr >= win_rate:
        response['action'] =  Actions.PUSH.value
    else:
        response['action'] =  Actions.FOLD.value

    return response
