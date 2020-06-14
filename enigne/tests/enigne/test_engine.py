import re
import time

from pytest import fixture

from enigne.board import Board, Move
from enigne.engine import Engine
from enigne.move_gen import legal_move_gen
from enigne.search import StatsSearchVisitor


@fixture
def engine():
    return Engine()


def test_engine_info(engine):
    info = engine.info()

    assert re.match(r'Enigne [0-9]+\.[0-9]+', info['name'])
    assert re.match(r'[A-Z][a-z]+ [A-Z][a-z]+(, [A-Z][a-z]+ [A-Z][a-z]+)*', info['author'])


def test_search_blocking(engine, initial_position_fen):
    engine.modify_position(initial_position_fen)
    start = time.perf_counter()
    move = engine.search(depth=3)
    assert time.perf_counter() - start > 0.03
    board = Board(initial_position_fen)
    assert move in set(legal_move_gen(board))


def test_search_non_blocking(engine, initial_position_fen):
    engine.modify_position(initial_position_fen)
    start = time.perf_counter()
    move = engine.search(depth=3, blocking=False)
    assert time.perf_counter() - start < 0.015
    assert not engine.search_done
    assert not move
    while not engine.search_done:
        time.sleep(0.003)
    assert time.perf_counter() - start > 0.03

    board = Board(initial_position_fen)
    assert engine.search_done in set(legal_move_gen(board))


def test_search_termination(engine, initial_position_fen):
    engine.modify_position(initial_position_fen)
    engine.search(depth=4, blocking=False)
    assert not engine.is_search_terminating
    start = time.perf_counter()
    engine.terminate_search()
    assert engine.is_search_terminating
    while not engine.search_done:
        time.sleep(0.001)
    assert time.perf_counter() - start < 0.003

    board = Board(initial_position_fen)
    assert engine.search_done in set(legal_move_gen(board))


def test_search_timeout(engine, initial_position_fen):
    engine.modify_position(initial_position_fen)
    start = time.perf_counter()
    move = engine.search(depth=4, timeout=0.1)
    assert 0.1 <= time.perf_counter() - start < 0.105
    board = Board(initial_position_fen)
    assert move in set(legal_move_gen(board))


def test_search_nodes(initial_position_fen):
    engine = Engine()
    visitor = StatsSearchVisitor()
    engine.set_search_visitor(visitor)
    engine.modify_position(initial_position_fen)
    start = time.perf_counter()
    move = engine.search(depth=4, nodes=100)
    assert visitor.nodes == 100
    assert time.perf_counter() - start < 0.1
    board = Board(initial_position_fen)
    assert move in set(legal_move_gen(board))


def test_search_filter_moves(engine, initial_position_fen):
    engine.modify_position(initial_position_fen)
    move = engine.search(depth=3, filter_moves=[Move.from_str("e2e4"), Move.from_str("h2h3")])
    assert str(move) in {"e2e4", "h2h3"}
