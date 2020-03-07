import pytest

from enigne.board import Board, Square
from enigne.move_gen import move_gen, attackers, is_attacked
from enigne.perft import perft
from tests.conftest import perfts, basic_fens


@pytest.mark.parametrize("basic_fen", [f for f in basic_fens() if f[2] is not None])
def test_move_gen(basic_fen):
    fen, _, moves_ref, *_ = basic_fen
    board = Board(fen)
    moves = list(move_gen(board))
    assert len(moves) == len(set(moves)), (board.fen(), ",".join(str(move) for move in moves))
    moves = set(str(move) for move in moves)
    assert moves == moves_ref


def test_attackers():
    board = Board('8/8/3pp3/2N1P3/8/8/8/8 b - - 0 1')
    assert set(attackers(board, Square.from_str('d6'), Board.WHITE)) == {Square.from_str('e5')}
    assert set(attackers(board, Square.from_str('e6'), Board.WHITE)) == {Square.from_str('c5')}

    assert is_attacked(board, Square.from_str('d6'), board.WHITE)
    assert not is_attacked(board, Square.from_str('a1'), Board.WHITE)


def _run_perft(perft_data, full=False):
    fen, node_counts, max_depth, divide_expected = perft_data
    board = Board(fen)
    for depth, nodes_expected in enumerate(node_counts, 1):
        if not full and depth > max_depth:
            break
        nodes, divide = perft(board, depth, divide=True)
        divide = {str(mv): count for mv, count in divide.items()}
        if divide_expected is None or depth < max_depth or depth > 2:
            assert nodes == nodes_expected, str(set(divide.keys()))
        else:
            assert divide == divide_expected
            assert nodes == nodes_expected


@pytest.mark.parametrize("perft_data", perfts())
def test_perft(perft_data):
    _run_perft(perft_data)


@pytest.mark.integtest
@pytest.mark.parametrize("perft_data", perfts())
def test_integration_perft(perft_data):
    _run_perft(perft_data, full=True)
