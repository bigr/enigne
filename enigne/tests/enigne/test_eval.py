import pytest

from enigne.board import Board
from enigne.eval import evaluate_material


@pytest.mark.parametrize('fen, score', [
    ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0),
    ('rnbqkbnr/pppppppp/8/8/8/8/8/RNBQKBNR w KQkq - 0 1', -8),
    ('rnbqkbnr/pppppppp/8/8/8/8/8/1NBQKBNR w KQkq - 0 1', -13),
    ('rnbqkbnr/pppppppp/8/8/8/8/8/2BQKBNR w KQkq - 0 1', -16),
    ('rnbqkbnr/pppppppp/8/8/8/8/8/3QKBNR w KQkq - 0 1', -19),
    ('rnbqkbnr/pppppppp/8/8/8/8/8/4KBNR w KQkq - 0 1', -28),
    ('rnbqkbnr/pppppppp/8/8/8/8/8/4K3 w KQkq - 0 1', -39),
    ('rnbqkbnr/pppppppp/8/8/8/8/8/4K3 b KQkq - 0 1', 39),
])
def test_evaluate_material(fen, score):
    board = Board(fen)
    assert evaluate_material(board) == score
