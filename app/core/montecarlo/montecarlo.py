#pylint: disable=C0114:missing-module-docstring
import os
import ctypes as ct

mc_lib = ct.CDLL(os.getcwd() + '/app/core/montecarlo/build/libMontecarlo.so')

calc_monte_carlo_c = mc_lib.calc_monte_carlo
calc_monte_carlo_c.argtypes = [
    ct.POINTER(ct.c_char_p),  # char **
    ct.POINTER(ct.c_char_p),  # char **
    ct.c_int]                 # int
calc_monte_carlo_c.restype = ct.c_int



def _convert_pylist_strings(values: list[str]):
    if values is None:
        raise ValueError(f"Parameter 'py_list' must be a Python list, not {type(values)}")

    c_array = (ct.c_char_p * len(values))()
    c_array[:] = values

    return c_array

def calc_montecarlo(hand: list[str], board: list[str]):
    """
    Calculates the Monte Carlo value of a hand against a board.
    """
    _hand = _convert_pylist_strings([c.encode() for c in hand])
    _board = _convert_pylist_strings([c.encode() for c in board])
    return calc_monte_carlo_c(_hand, _board, len(board))


if __name__ == '__main__':
    print(calc_montecarlo(['As', 'Ks'], ['Ad', 'Kd', '2h']))