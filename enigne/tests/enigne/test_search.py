import pytest

from enigne.board import Board
from enigne.search import alphabeta_search, MATE_SCORE


@pytest.mark.parametrize('fen, depth, expected_score, pvs', [
    ('7k/8/8/8/3r4/8/2r5/K7 b - - 0 1', 2, MATE_SCORE, {'d4d1'}),
    ('7k/8/8/8/3r4/8/4r3/K7 w - - 0 1', 3, -MATE_SCORE, {'a1b1 d4d1'}),
    ('7k/4Q3/8/6K1/8/8/8/8 w - - 0 1', 4, MATE_SCORE,
        {'g5f6 h8g8 e7g7', 'g5g6 h8g8 e7g7', 'g5h6 h8g8 e7g7', 'g5g6 h8g8 e7e8', 'g5g6 h8g8 e7d8', 'g5h6 h8g8 e7e8'}),
])
def test_alphabeta_search(fen, depth, expected_score, pvs):
    board = Board(fen)
    score, pv = alphabeta_search(board, depth)
    assert score == expected_score
    assert len(pv) <= depth

    assert " ".join(str(mv) for mv in pv) in pvs

    for i, move in enumerate(pv, 1):
        board.move(move)
        score, _ = alphabeta_search(board, depth - i)
        assert score == expected_score * (-1 if i % 2 else 1)
