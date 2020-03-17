from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from typing import Optional, Dict, Iterable, Union

import enigne
from .board import Move, Board
from .search import SearchVisitor, alphabeta_search, BagOfSearchVisitors, PVSearchVisitor, TimeoutHaltSearchVisitor, \
    NodesCountHaltSearchVisitor, FilterMovesSearchVisitor


class EngineBase(ABC):
    _search_visitor: Optional[SearchVisitor]

    def __init__(self):
        self._search_visitor = None

    def set_search_visitor(self, _search_visitor: SearchVisitor):
        self._search_visitor = _search_visitor

    @abstractmethod
    def info(self) -> Dict[str, str]:
        pass

    @property
    @abstractmethod
    def search_done(self) -> Optional[Move]:
        """Returns searched move if non blocking search is done, otherwise returns `None`"""
        pass

    @property
    @abstractmethod
    def search_in_progress(self) -> bool:
        pass

    @abstractmethod
    def new_game(self) -> None:
        pass

    @abstractmethod
    def modify_position(self, fen: Optional[str] = None, moves: Optional[Iterable[Move]] = None) -> None:
        pass

    @abstractmethod
    def search(self, depth: Optional[int] = None, nodes: Optional[int] = None,
               filter_moves: Optional[Iterable[Move]] = None, timeout: Optional[float] = None,
               blocking: bool = True) -> Union[None, Move]:
        """
        Search current position for best moves.
        :param depth: maximal depth to search (in plies).
        :param nodes: maximal nodes to search
        :param filter_moves: restrict search to this moves only
        :param timeout: maximal duration of search (in seconds)
        :param blocking: If `false` this method is not blocking and result have to be read with some search visitors
        :return:
        If `blocking` is `True` best move is returned, otherwise `None`.
        """
        pass

    @abstractmethod
    def search_mate(self, depth: Optional[int] = None, nodes: Optional[int] = None,
                    filter_moves: Optional[Iterable[Move]] = None, timeout: Optional[float] = None,
                    blocking: bool = False) -> Union[None, Move]:
        """Same as `search` method but finds out only mates."""
        pass

    @abstractmethod
    def terminate_search(self):
        """Halts search (running in non blocking mode) as soon as possible."""
        pass

    @property
    @abstractmethod
    def is_search_terminating(self) -> bool:
        """`True` if `terminate_search` was called but search is not terminated yet."""
        pass

    @abstractmethod
    def quit(self):
        pass


class EngineHaltSearchVisitor(SearchVisitor):
    _engine: EngineBase
    _child: EngineHaltSearchVisitor

    def __init__(self, engine: EngineBase, parent: Optional[SearchVisitor] = None):
        super().__init__(parent=parent)
        self._engine = engine

    def _create_child(self) -> EngineHaltSearchVisitor:
        return EngineHaltSearchVisitor(self._engine, parent=self)

    @property
    def halt(self) -> bool:
        return self._engine.is_search_terminating


class Engine(EngineBase):
    _board: Optional[Board]
    _search_thread: Optional[threading.Thread]
    _terminate_search: bool
    _search_done: Optional[Move]

    def __init__(self):
        super().__init__()
        self._board = None
        self._search_thread = None
        self._terminate_search = False
        self._search_done = None

    def info(self) -> Dict[str, str]:
        return {
            'author': enigne.__author__,
            'name': f'{enigne.__name__} {enigne.__version__}',
        }

    @property
    def search_done(self) -> Optional[Move]:
        return self._search_done

    @property
    def search_in_progress(self) -> bool:
        return not self._search_done and self._search_thread

    def new_game(self) -> None:
        pass

    def modify_position(self, fen: Optional[str] = None, moves: Optional[Iterable[Move]] = None) -> None:
        if fen:
            self._board = Board(fen)
        if moves:
            for move in moves:
                self._board.move(move)

    def search(self, depth: Optional[int] = None, nodes: Optional[int] = None,
               filter_moves: Optional[Iterable[Move]] = None, timeout: Optional[float] = None,
               blocking: bool = True) -> Union[None, Move]:

        def do_search():
            try:
                visitors = {
                    'halt': EngineHaltSearchVisitor(self),
                    'pv': PVSearchVisitor()
                }
                if timeout:
                    visitors['timeout_halt'] = TimeoutHaltSearchVisitor(timeout)
                if nodes:
                    visitors['nodes_halt'] = NodesCountHaltSearchVisitor(nodes)
                if filter_moves:
                    visitors['filter_moves'] = FilterMovesSearchVisitor(list(filter_moves))
                if self._search_visitor:
                    visitors['custom'] = self._search_visitor

                visitor = BagOfSearchVisitors(visitors)

                alphabeta_search(self._board, depth, visitor=visitor)

                self._search_done = visitors['pv'].best_move
                return visitors['pv'].best_move
            except:
                self._search_done = 'ERROR'
                raise

        if blocking:
            return do_search()
        else:
            self._search_thread = threading.Thread(target=do_search, args=())
            self._terminate_search = False
            self._search_done = None
            self._search_thread.start()
            return None

    def search_mate(self, depth: Optional[int] = None, nodes: Optional[int] = None,
                    filter_moves: Optional[Iterable[Move]] = None, timeout: Optional[float] = None,
                    blocking: bool = False) -> Union[None, Move]:

        raise NotImplementedError()

    def terminate_search(self):
        self._terminate_search = True

    @property
    def is_search_terminating(self) -> bool:
        return self._terminate_search

    def quit(self):
        if self._search_thread:
            self.terminate_search()
            self._search_thread.join()
