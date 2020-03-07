import pytest
import math

from enigne.board import Board
from enigne.search import alphabeta_search


@pytest.mark.parametrize('fen, depth, score', [
    ('8/2k5/5p2/4P3/8/4K3/8/8 b - - 0 1', 1, 1),
    ('8/2k5/5p2/4P3/8/4K3/8/8 w - - 0 1', 1, 1),
    ('8/2k5/3n1p2/4P3/8/4K3/8/8 w - - 0 1', 1, 0),
    ('8/2k5/3n1p2/4P3/8/4K3/8/8 b - - 0 1', 1, 4),
    ('8/1k6/8/8/8/6pp/8/5r1K w - - 0 1', 1, -math.inf),
    ('8/8/8/8/8/6p1/5k2/7K w - - 0 1', 1, 0),
    ('K7/3N4/8/3p4/3P4/8/6k1/8 w - - 0 1', 1, 3),
    ('K7/3N4/8/3p4/3P4/8/6k1/8 w - - 0 1', 2, 3),
    ('K7/3N4/8/3p4/3P4/8/6k1/8 w - - 0 1', 3, 4),
])
def test_alphabeta_search(fen, depth, score):
    board = Board(fen)
    assert alphabeta_search(board, depth) == score
