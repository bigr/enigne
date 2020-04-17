from __future__ import annotations

import math
import time
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
    _halt: bool

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

    @property
    def halt(self):
        """If this method returns `true` search is stopped immediately."""
        return False

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


class StatsSearchVisitor(SearchVisitor):
    _nodes: int
    _start_clock: Optional[float]
    _end_clock: Optional[float]

    def __init__(self, parent: Optional[SearchVisitor] = None):
        super().__init__(parent=parent)
        self._nodes = 0
        self._start_clock = None
        self._end_clock = None
        self._pv = []

    @property
    def nodes(self):
        return self._nodes

    @property
    def duration(self) -> Optional[float]:
        if not self._start_clock:
            return None
        elif not self._end_clock:
            return time.perf_counter() - self._start_clock
        else:
            return self._end_clock - self._start_clock

    def current_move(self, move: Move) -> None:
        self._inc_nodes()

    def _inc_nodes(self):
        if self.parent:
            self.parent._inc_nodes()
        else:
            self._nodes += 1

    def start(self):
        self._start_clock = time.perf_counter()

    def end(self):
        self._end_clock = time.perf_counter()


class BagOfSearchVisitors(SearchVisitor):
    _visitors: Dict[str, SearchVisitor]

    def __init__(self, visitors: Dict[str, SearchVisitor], parent: Optional[str, SearchVisitor] = None, **kwargs):
        super().__init__(visitors, parent=parent, **kwargs)
        if parent is None:
            self._visitors = visitors
        else:
            self._visitors = {
                name: visitor.__class__(*visitor._init_args, parent=visitor, **visitor._init_kwargs)
                for name, visitor in visitors.items()
            }
            for name, visitor in visitors.items():
                visitor._child = self._visitors[name]

    @property
    def visitors(self) -> Dict[str, SearchVisitor]:
        return self._visitors

    @property
    def halt(self):
        return any(visitor.halt for visitor in self.visitors.values())

    def start(self):
        for visitor in self.visitors.values():
            visitor.start()

    def end(self):
        for visitor in self.visitors.values():
            visitor.end()

    def new_best_move(self, score: float, is_principal_variation=False) -> None:
        for visitor in self.visitors.values():
            visitor.new_best_move(score, is_principal_variation=is_principal_variation)

    def current_move(self, move: Move) -> None:
        for visitor in self.visitors.values():
            visitor.current_move(move)

    def mated(self) -> None:
        for visitor in self.visitors.values():
            visitor.mated()

    def stalemated(self) -> None:
        for visitor in self.visitors.values():
            visitor.stalemated()


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
            if visitor.halt:
                return score

        if mate:
            if in_check(board):
                visitor.mated()
                return -MATE_SCORE
            else:
                visitor.stalemated()
                return 0

        return alpha
