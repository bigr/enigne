import math

from enigne.board import Board
from enigne.eval import evaluate_material
from enigne.move_gen import legal_move_gen, in_check


def alphabeta_search(board: Board, depth: int, alpha: float = -math.inf, beta: float = math.inf):
    if depth == 0:
        return evaluate_material(board)

    value = -math.inf
    mate = True
    for move in legal_move_gen(board):
        mate = False
        with board.do_move(move):
            value = max(value, -alphabeta_search(board, depth - 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
    if mate and not in_check(board):
        value = 0

    return value
