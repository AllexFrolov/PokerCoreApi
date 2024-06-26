from flask_restx import fields
from enum import Enum

from config import COMBINATIONS_NAME

class Actions(Enum):
    ALL_IN: str = 'ALL_IN'
    FOLD: str = 'FOLD'
    RAISE: str = 'RAISE'
    CALL: str = 'CALL'
    CHECK: str = 'CHECK'


class PokerStage(Enum):
    PREFLOP = 'PREFLOP'
    FLOP = 'FLOP'
    TURN = 'TURN'
    RIVER = 'RIVER'

class PlayerTypes(Enum):
    HERO = 'HERO'
    OPP_1 = 'OPP_1'
    OPP_2 = 'OPP_2'
    OPP_3 = 'OPP_3'
    OPP_4 = 'OPP_4'
    OPP_5 = 'OPP_5'
    OPP_6 = 'OPP_6'
    OPP_7 = 'OPP_7'
    OPP_8 = 'OPP_8'
    
    @classmethod
    def opps(cls):
        return [v for k, v in cls.__dict__.items() if 'OPP' in k]
    
class PossibleCombs(fields.Raw):
    __schema_type__ = 'json'
    __schema_example__ = {
        'value': [1/len(COMBINATIONS_NAME)]*len(COMBINATIONS_NAME),
        'names': COMBINATIONS_NAME
                          }
