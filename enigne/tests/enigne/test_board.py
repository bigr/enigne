from enigne.board import Board, Square, File, Rank, SquareStr, Move, MoveStr


def test_square_eq():
    assert Square(File(2), Rank(3)) == Square(File(2), Rank(3))
    assert Square(File(1), Rank(2)) != Square(File(2), Rank(1))


def test_square_str():
    assert str(Square(File(1), Rank(4))) == 'b5'


def test_square_from_str():
    assert str(Square.from_str(SquareStr('c6'))) == 'c6'


def test_move_eq():
    assert \
        Move(Square.from_str(SquareStr('a3')), Square.from_str(SquareStr('a4'))) == \
        Move(Square.from_str(SquareStr('a3')), Square.from_str(SquareStr('a4')))

    assert \
        Move(Square.from_str(SquareStr('e2')), Square.from_str(SquareStr('e4'))) != \
        Move(Square.from_str(SquareStr('a3')), Square.from_str(SquareStr('a4')))

    assert \
        Move(Square.from_str(SquareStr('b2')), Square.from_str(SquareStr('a1')), Board.QUEEN) == \
        Move(Square.from_str(SquareStr('b2')), Square.from_str(SquareStr('a1')), Board.QUEEN)

    assert \
        Move(Square.from_str(SquareStr('b2')), Square.from_str(SquareStr('a1')), Board.QUEEN) != \
        Move(Square.from_str(SquareStr('b2')), Square.from_str(SquareStr('a1')), Board.ROOK)


def test_move_str():
    assert str(Move(Square.from_str(SquareStr('a3')), Square.from_str(SquareStr(SquareStr('a4'))))) == 'a3a4'
    assert \
        str(Move(Square.from_str(SquareStr('b2')), Square.from_str(SquareStr(SquareStr('a1'))), Board.QUEEN)) == 'b2a1q'


def test_move_from_str():
    assert str(Move.from_str(MoveStr('a3a4'))) == 'a3a4'
    assert str(Move.from_str(MoveStr('b2a1q'))) == 'b2a1q'


def test_fen(basic_fens):
    for fen, *_ in basic_fens:
        assert Board(fen).fen() == fen
