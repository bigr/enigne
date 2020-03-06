import pytest

from enigne.board import Board
from enigne.move_gen import move_gen

from tests.conftest import basic_fens


@pytest.mark.parametrize("basic_fen", [f for f in basic_fens() if f[2] is not None])
def test_move_gen(basic_fen):
    fen, _, moves_ref, *_ = basic_fen
    board = Board(fen)
    moves = list(move_gen(board))
    assert len(moves) == len(set(moves)), (board.fen(), ",".join(str(move) for move in moves))
    moves = set(str(move) for move in moves)
    assert moves == moves_ref
