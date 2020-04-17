import time

import pytest

from enigne.board import Board, Move
from enigne.search import alphabeta_search, MATE_SCORE, SearchVisitor, PVSearchVisitor, StatsSearchVisitor, \
    BagOfSearchVisitors


def test_search_visitor():
    visitor = SearchVisitor()
    with visitor.child() as child_visitor:
        assert child_visitor.parent == visitor


def test_pv_search_visitor():
    visitor = PVSearchVisitor()
    visitor.current_move(Move.from_str('e2e3'))
    visitor.current_move(Move.from_str('e2e4'))
    visitor.new_best_move(0, is_principal_variation=True)
    visitor.current_move(Move.from_str('f2f4'))
    assert str(visitor.best_move) == 'e2e4'
    assert " ".join([str(mv) for mv in visitor.pv]) == 'e2e4'
    with visitor.child() as child_visitor:
        child_visitor.current_move(Move.from_str('e7e6'))
        child_visitor.new_best_move(0, is_principal_variation=True)
        child_visitor.current_move(Move.from_str('e7e5'))
        child_visitor.new_best_move(0.1, is_principal_variation=True)
        child_visitor.current_move(Move.from_str('f7f5'))
    assert str(visitor.best_move) == 'f2f4'
    assert " ".join([str(mv) for mv in visitor.pv]) == 'f2f4 e7e5'


def test_stats_search_visitor():
    visitor = StatsSearchVisitor()
    time.sleep(0.01)
    with visitor:
        visitor.current_move(Move.from_str('e2e3'))
        time.sleep(0.005)
        visitor.current_move(Move.from_str('e2e4'))
        with visitor.child() as child_visitor:
            with child_visitor:
                child_visitor.current_move(Move.from_str('e7e5'))
                child_visitor.current_move(Move.from_str('e7e6'))
                time.sleep(0.005)
                child_visitor.new_best_move(0, is_principal_variation=True)
        time.sleep(0.005)
        visitor.current_move(Move.from_str('f2f4'))
    time.sleep(0.01)
    assert 0.015 <= visitor.duration < 0.0175
    assert visitor.nodes == 5


def test_bag_of_search_visitors():
    visitor = BagOfSearchVisitors({
        'pv': PVSearchVisitor(),
        'stats': StatsSearchVisitor()
    })
    with visitor:
        visitor.current_move(Move.from_str('e2e3'))
        time.sleep(0.005)
        visitor.current_move(Move.from_str('e2e4'))
        with visitor.child() as child_visitor:
            assert child_visitor.visitors is not None
            assert child_visitor.visitors != visitor.visitors
            with child_visitor:
                child_visitor.current_move(Move.from_str('e7e5'))
                child_visitor.current_move(Move.from_str('e7e6'))
                child_visitor.new_best_move(0, is_principal_variation=True)
                time.sleep(0.005)
                child_visitor.current_move(Move.from_str('f7f5'))
        time.sleep(0.005)
        visitor.current_move(Move.from_str('f2f4'))
    time.sleep(0.01)
    assert str(visitor.visitors['pv'].best_move) == 'e2e4'
    assert " ".join([str(mv) for mv in visitor.visitors['pv'].pv]) == 'e2e4 e7e6'
    assert 0.015 <= visitor.visitors['stats'].duration < 0.0175
    assert visitor.visitors['stats'].nodes == 6


@pytest.mark.parametrize('fen, depth, expected_score, pvs', [
    ('7k/8/8/8/3r4/8/2r5/K7 b - - 0 1', 2, MATE_SCORE, {'d4d1'}),
    ('7k/8/8/8/3r4/8/4r3/K7 w - - 0 1', 3, -MATE_SCORE, {'a1b1 d4d1'}),
    ('7k/4Q3/8/6K1/8/8/8/8 w - - 0 1', 4, MATE_SCORE,
        {'g5f6 h8g8 e7g7', 'g5g6 h8g8 e7g7', 'g5h6 h8g8 e7g7', 'g5g6 h8g8 e7e8', 'g5g6 h8g8 e7d8', 'g5h6 h8g8 e7e8'}),
])
def test_alphabeta_search(fen, depth, expected_score, pvs):
    board = Board(fen)
    score = alphabeta_search(board, depth)
    assert score == expected_score
    for pv in list(pvs)[:1]:
        pv = [Move.from_str(mv) for mv in pv.split()]
        for i, move in enumerate(pv, 1):
            board.move(move)
            score = alphabeta_search(board, depth - i)
            assert score == expected_score * (-1 if i % 2 else 1)


@pytest.mark.parametrize('fen, depth, expected_score, pvs', [
    ('7k/8/8/8/3r4/8/2r5/K7 b - - 0 1', 2, MATE_SCORE, {'d4d1'}),
    ('7k/8/8/8/3r4/8/4r3/K7 w - - 0 1', 3, -MATE_SCORE, {'a1b1 d4d1'}),
    ('7k/4Q3/8/6K1/8/8/8/8 w - - 0 1', 4, MATE_SCORE,
        {'g5f6 h8g8 e7g7', 'g5g6 h8g8 e7g7', 'g5h6 h8g8 e7g7', 'g5g6 h8g8 e7e8', 'g5g6 h8g8 e7d8', 'g5h6 h8g8 e7e8'}),
])
def test_pv_search_visitor_in_alphabeta_search(fen, depth, expected_score, pvs):
    board = Board(fen)
    visitor = PVSearchVisitor()
    alphabeta_search(board, depth, visitor=visitor)
    assert " ".join(str(mv) for mv in visitor.pv) in pvs



