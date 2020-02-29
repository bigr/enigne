from enigne.board import Board
from enigne.move_gen import move_gen


def test_move_gen(basic_fens):
    for fen, _, moves_ref, *_ in basic_fens:
        if moves_ref is None:
            continue

        board = Board(fen)
        moves = set(str(move) for move in move_gen(board))
        assert moves == moves_ref
