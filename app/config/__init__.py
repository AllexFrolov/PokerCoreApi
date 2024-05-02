DEFAULT_RANGE = 0.3
DEFAULT_WR_CUM = 0.55

CARD_RANKS = {rank: idx for idx, rank in enumerate('23456789TJQKA')}
CARD_SUITS = {suit: idx for idx, suit in enumerate('shdc')}

COMBINATIONS_NAME = [
    'straught_flush',
    'four_of_a kind',
    'full_house',
    'flush',
    'straight',
    'three_of_a_kind',
    'two_pair',
    'one_pair',
    'high_card']