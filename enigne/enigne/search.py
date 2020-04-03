from __future__ import annotations

import math
from typing import Tuple, List, Optional, Iterator, Dict, Any
from contextlib import contextmanager

from enigne.board import Board, Move
from enigne.eval import evaluate_material
from enigne.move_gen import legal_move_gen, in_check

MATE_SCORE = 32767


class SearchVisitor:
    _parent: Optional[SearchVisitor]
    _child: Optional[SearchVisitor]
    _init_kwargs: Dict[Any]
    _init_args: Tuple[Any]

    def __init__(self, *args, parent: Optional[SearchVisitor] = None, **kwargs):
        self._parent = parent
        self._init_kwargs = kwargs
        self._init_args = args
        self._child = None

    @property
    def parent(self) -> Optional[SearchVisitor]:
        return self._parent

    @contextmanager
    def child(self) -> Iterator[SearchVisitor]:
        self._child = self.__class__(*self._init_args, parent=self, **self._init_kwargs)
        try:
            yield self._child
        finally:
            pass

    def start(self):
        pass

    def end(self):
        pass

    def new_best_move(self, score: float, is_principal_variation=False) -> None:
        pass

    def current_move(self, move: Move) -> None:
        pass

    def mated(self) -> None:
        pass

    def stalemated(self) -> None:
        pass

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()


def alphabeta_search(board: Board, depth: int, alpha: float = -math.inf,
                     beta: float = math.inf) -> Tuple[float, List[Move]]:
    """Negamax implementation of alpha-beta pruning."""
    if depth == 0:
        return evaluate_material(board), []

    pv = []
    mate = True
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
