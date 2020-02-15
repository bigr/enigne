from enigne.board import Board


def test_fen(basic_fens):
    for fen, *_ in basic_fens:
        assert Board(fen).fen() == fen
