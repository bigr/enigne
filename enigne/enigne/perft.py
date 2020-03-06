from typing import Dict, Union, Tuple

from .board import Board, Move
from .move_gen import legal_move_gen


def perft(board: Board, depth: int, divide: bool = False) -> Union[int, Tuple[int, Dict[Move, int]]]:
    if depth == 0:
        return 1

    total_nodes = 0
    moves: Dict[Move, int] = {}
    for move in legal_move_gen(board):
        with board.do_move(move):
            move_nodes = perft(board, depth - 1)
            total_nodes += move_nodes
            if divide:
                if move in moves:
                    assert False
                moves[move] = move_nodes
    if divide:
        return total_nodes, moves
    else:
        return total_nodes
