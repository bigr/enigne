from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Dict, Iterable, Union

from .board import Move
from .search import SearchVisitor


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

    def __init__(self, engine: EngineBase, parent: Optional[SearchVisitor] = None):
        super().__init__(engine, parent=parent)
        self._engine = engine

    @property
    def halt(self) -> bool:
        return self._engine.is_search_terminating
