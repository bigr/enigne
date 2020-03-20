import math
from typing import Tuple, List

from enigne.board import Board, Move
from enigne.eval import evaluate_material
from enigne.move_gen import legal_move_gen, in_check


def alphabeta_search(board: Board, depth: int, alpha: float = -math.inf,
                     beta: float = math.inf) -> Tuple[float, List[Move]]:
    if depth == 0:
        return evaluate_material(board), []

    pv = []
    value = -math.inf
    mate = True
    for move in legal_move_gen(board):
        mate = False
        with board.do_move(move):
            sub_value, sub_pv = alphabeta_search(board, depth - 1, alpha, beta)
            if -sub_value > value:
                value = -sub_value
                pv = [move] + sub_pv
            alpha = max(alpha, value)
            if alpha >= beta:
                break
    if mate and not in_check(board):
        value = 0

    return value, pv
