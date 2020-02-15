from enigne.board import Board, Square, File, Rank, SquareStr


def test_square_equ():
    assert Square(File(2), Rank(3)) == Square(File(2), Rank(3))
    assert Square(File(1), Rank(2)) != Square(File(2), Rank(1))


def test_square_str():
    assert str(Square(File(1), Rank(4))) == 'b5'


def test_square_from_str():
    assert str(Square.from_str(SquareStr('c6'))) == 'c6'


def test_fen(basic_fens):
    for fen, *_ in basic_fens:
        assert Board(fen).fen() == fen
