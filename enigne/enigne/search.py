import math
from typing import Tuple, List

from enigne.board import Board, Move
from enigne.eval import evaluate_material
from enigne.move_gen import legal_move_gen, in_check

MATE_SCORE = 32767


def alphabeta_search(board: Board, depth: int, alpha: float = -math.inf,
                     beta: float = math.inf) -> Tuple[float, List[Move]]:
    """Negamax implementation of alpha-beta pruning."""
    if depth == 0:
        return evaluate_material(board), []

    pv = []
    mate = True
    score_mx = -math.inf
    for move in legal_move_gen(board):
        mate = False
        with board.do_move(move):
            score, sub_pv = alphabeta_search(board, depth - 1, -beta, -alpha)
        score *= -1
        if score >= beta and score != math.inf:
            return beta, pv
        if score > alpha:
            alpha = score
            pv = [move] + sub_pv

    if mate:
        return (-MATE_SCORE if in_check(board) else 0), []

    return alpha, pv
