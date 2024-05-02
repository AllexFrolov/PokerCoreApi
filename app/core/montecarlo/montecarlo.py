#pylint: disable=C0114:missing-module-docstring
import os
import ctypes as ct
from sys import platform

from config import COMBINATIONS_NAME
from logger import get_logger
logger = get_logger()

if platform == "linux" or platform == "linux2":
    mc_lib = ct.CDLL(os.getcwd() + '/core/montecarlo/build/libMontecarlo.so')
else:
    mc_lib = ct.CDLL(os.getcwd() + '/core/montecarlo/build/libMontecarlo.dll')

hero_vs_range_c = mc_lib.hero_vs_range
hero_vs_range_c.argtypes = [
    ct.POINTER(ct.c_char_p),                # char ** (Hero cards)
    ct.POINTER(ct.POINTER(ct.c_char_p)),    # char *** (Opponent range)
    ct.c_int,                               # int     (range size)
    ct.POINTER(ct.c_char_p),                # char ** (Board cards)
    ct.c_int,                               # int     (Board size)
    ct.c_uint]                              # unsigned int (Number of iterations)
hero_vs_range_c.restype = ct.c_double

possible_combinations_c = mc_lib.possible_combinations
possible_combinations_c.argtypes = [
    ct.POINTER(ct.c_char_p),                # char ** (Hero cards)
    ct.POINTER(ct.POINTER(ct.c_char_p)),    # char *** (Opponent range)
    ct.c_int,                               # int     (range size)
    ct.POINTER(ct.c_char_p),                # char ** (Board cards)
    ct.c_int]                              # int     (Board size)

possible_combinations_c.restype = ct.POINTER(ct.c_int)

free_memory_c = mc_lib.free_int_arr
free_memory_c.argtypes = [ct.POINTER(ct.c_int)]
free_memory_c.restype = None


def _convert_list_str(values: list[str]):
    if values is None:
        raise ValueError(f"Parameter 'py_list' must be a Python list, not {type(values)}")

    c_array = (ct.c_char_p * len(values))()
    c_array[:] = [v.encode('utf-8') for v in values]

    return c_array

def _convert_list_list_str(values: list[list[str]]):
    c_array = (ct.POINTER(ct.c_char_p) * len(values))()

    for i, sublist in enumerate(values):
        arr = (ct.c_char_p * len(sublist))()
        arr[:] = [ct.c_char_p(item.encode('utf-8')) for item in sublist]
        c_array[i] = arr
    return c_array

def hero_vs_range(
        hero_hand: list[str],
        opp_range: list[list[str]],
        board: list[str],
        iters_per_hand: int=100
        ) -> float:
    """
    Calculates the Monte Carlo value of a hand against a board.
    """
    _hero_hand = _convert_list_str(hero_hand)
    _opp_range = _convert_list_list_str(opp_range)
    _board = _convert_list_str(board)
    _iterations = ct.c_uint(iters_per_hand)

    response = hero_vs_range_c(
        _hero_hand,
        _opp_range,
        len(_opp_range),
        _board,
        len(board),
        _iterations)

    return response


def possible_combinations(
        hero_hand: list[str],
        opp_range: list[list[str]],
        board: list[str]) -> tuple[list[int], list[str]]:
    """
    Evaluete all hand in opp range and counting posible combinations
    """
    
    if len(board) != 0:
        _hero_hand = _convert_list_str(hero_hand)
        _opp_range = _convert_list_list_str(opp_range)
        _board = _convert_list_str(board)

        c_int_pointer = possible_combinations_c(
            _hero_hand,
            _opp_range,
            len(_opp_range),
            _board,
            len(board))
        comb_values = [c_int_pointer[i] for i in range(len(COMBINATIONS_NAME))]
        free_memory_c(c_int_pointer)
    else:
        comb_values = [0] * len(COMBINATIONS_NAME)
        for hand in opp_range:
            if hand[0][0] == hand[1][0]:
                comb_values[-2] += 1
            else:
                comb_values[-1] += 1
    
    comb_values_sum = sum(comb_values)
    comb_values = [value / comb_values_sum for value in comb_values]

    return comb_values, COMBINATIONS_NAME
    