import json
import os
from config.config import (
    DEFAULT_RANGE, 
    DEFAULT_WR_CUM,
    CARD_RANKS,
    )

from schemas import Actions


with open('./app/data/hands_range.json', 'r') as f:
    hands_range =  json.loads(f.read())

with open('./app/data/hands.json', 'r') as f:
    hands_combination = json.loads(f.read())


def make_action(hand: list[str],  hand_range=DEFAULT_RANGE) -> str:
    hand.sort(key=lambda x: CARD_RANKS[x[0]], reverse=True)
    hand_str = ''.join(map(str, hand))
    r = hands_range[hands_combination[hand_str]]['range']
    if r <= DEFAULT_RANGE:
        return Actions.PUSH.value
    return Actions.FOLD.value
