import json

from config.config import (
    DEFAULT_RANGE, 
    DEFAULT_WR_CUM,
    CARD_RANKS,
    CARD_SUITS
    )

from schemas import Actions

from .montecarlo import calc_montecarlo



with open('./data/hands_range.json', 'r') as f:
    hands_range =  json.loads(f.read())

with open('./data/hands.json', 'r') as f:
    hands_combination = json.loads(f.read())


def make_action(hand: list[str], board: list[str]=list(), hand_range: float=None, win_rate: float=None) -> str:
    wr = calc_montecarlo(hand, board)
    
    if win_rate is None:
        win_rate = DEFAULT_WR_CUM
                
    if wr >= win_rate:
        return Actions.PUSH.value
                
    return Actions.FOLD.value
