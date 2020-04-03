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


class PVSearchVisitor(SearchVisitor):
    """Search visitor logging principal variation"""

    _current_move: Optional[Move]
    _best_move: Optional[Move]
    _pv: List[Move]

    def __init__(self, parent: Optional[SearchVisitor] = None):
        super().__init__(parent=parent)
        self._current_move = None
        self._best_move = None
        self._pv = []

    @property
    def best_move(self) -> Optional[Move]:
        return self._best_move

    @property
    def pv(self) -> Optional[List[Move]]:
        return self._pv

    def current_move(self, move: Move) -> None:
        self._current_move = move

    def new_best_move(self, score: float, is_principal_variation=False) -> None:
        self._best_move = self._current_move
        if is_principal_variation:
            self._pv = [self._best_move] + (self._child.pv if self._child else [])
            if self.parent:
                self.parent.new_best_move(-score, is_principal_variation=True)


def alphabeta_search(board: Board, depth: int, alpha: float = -math.inf,
                     beta: float = math.inf, visitor: SearchVisitor = SearchVisitor()) -> float:
    """Negamax implementation of alpha-beta pruning."""
    with visitor:
        if depth == 0:
            return evaluate_material(board)

        mate = True
        for move in legal_move_gen(board):
            visitor.current_move(move)
            mate = False
            with board.do_move(move), visitor.child() as child_visitor:
                score = alphabeta_search(board, depth - 1, -beta, -alpha, child_visitor)
            score *= -1
            if score >= beta and score != math.inf:
                visitor.new_best_move(score)
                return beta
            if score > alpha:
                visitor.new_best_move(score, is_principal_variation=True)
                alpha = score

        if mate:
            if in_check(board):
                visitor.mated()
                return -MATE_SCORE
            else:
                visitor.stalemated()
                return 0

        return alpha
