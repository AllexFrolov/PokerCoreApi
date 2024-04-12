#pylint: disable=C0114:missing-module-docstring
import os
import ctypes as ct

mc_lib = ct.CDLL(os.getcwd() + '/app/core/montecarlo/build/libMontecarlo.so')

calc_monte_carlo = mc_lib.calc_monte_carlo
calc_monte_carlo.argtypes = [ct.POINTER(ct.c_char), ct.POINTER(ct.c_char), ct.c_int]
calc_monte_carlo.restype = ct.c_int

if __name__ == '__main__':
    hand = (ct.c_char * 2)()
    hand[0] = b'A'
    hand[1] = b'K'
    board = (ct.c_char * 2)()
    board[0] = b'A'
    board[1] = b'K'
    print(calc_monte_carlo(hand, board, len(board)))
