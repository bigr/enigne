from enigne.board import Board, Square, File, Rank, Move


def test_square_eq():
    assert Square(File(2), Rank(3)) == Square(File(2), Rank(3))
    assert Square(File(1), Rank(2)) != Square(File(2), Rank(1))


def test_square_str():
    assert str(Square(File(1), Rank(4))) == 'b5'


def test_square_from_str():
    assert str(Square.from_str('c6')) == 'c6'


def test_square_is_valid():
    assert all(Square(File(file), Rank(rank)).is_valid() for file in range(8) for rank in range(8))
    assert not Square(File(-1), Rank(4)).is_valid()
    assert not Square(File(8), Rank(4)).is_valid()
    assert not Square(File(3), Rank(-1)).is_valid()
    assert not Square(File(3), Rank(8)).is_valid()


def test_move_eq():
    assert \
        Move(Square.from_str('a3'), Square.from_str('a4')) == \
        Move(Square.from_str('a3'), Square.from_str('a4'))

    assert \
        Move(Square.from_str('e2'), Square.from_str('e4')) != \
        Move(Square.from_str('a3'), Square.from_str('a4'))

    assert \
        Move(Square.from_str('b2'), Square.from_str('a1'), Board.QUEEN) == \
        Move(Square.from_str('b2'), Square.from_str('a1'), Board.QUEEN)

    assert \
        Move(Square.from_str('b2'), Square.from_str('a1'), Board.QUEEN) != \
        Move(Square.from_str('b2'), Square.from_str('a1'), Board.ROOK)


def test_move_str():
    assert str(Move(Square.from_str('a3'), Square.from_str('a4'))) == 'a3a4'
    assert \
        str(Move(Square.from_str('b2'), Square.from_str('a1'), Board.QUEEN)) == 'b2a1q'


def test_move_from_str():
    assert str(Move.from_str('a3a4')) == 'a3a4'
    assert str(Move.from_str('b2a1q')) == 'b2a1q'


def test_fen(basic_fens):
    for fen, *_ in basic_fens:
        assert Board(fen).fen() == fen


def test_board_set_get():
    board = Board()
    sq = Square.from_str('b2')
    assert board[sq] is None
    for piece in {(Board.PAWN, Board.WHITE), (Board.BISHOP, Board.BLACK)}:
        board[sq] = piece
        assert board[sq] == piece
    board[sq] = None
    assert board[sq] is None
    assert board.fen() == Board().fen()


def test_board_pieces(basic_fens):
    board = Board(basic_fens[0][0])
    assert board.own_pieces(Square.from_str('e2')) == Board.PAWN
    assert board.own_pieces(Square.from_str('e1')) == Board.KING
    assert board.own_pieces(Square.from_str('e1'), Board.KING) == Board.KING
    assert board.own_pieces(Square.from_str('e1'), Board.PAWN) is None
    assert board.own_pieces(Square.from_str('e7')) is None
    assert board.own_pieces(Square.from_str('e5')) is None
    assert board.opponent_pieces(Square.from_str('e2')) is None
    assert board.opponent_pieces(Square.from_str('e7')) == Board.PAWN
    assert board.opponent_pieces(Square.from_str('e5')) is None
    board.turn = Board.BLACK
    assert board.own_pieces(Square.from_str('e2')) is None
    assert board.own_pieces(Square.from_str('e7')) == Board.PAWN
    assert board.own_pieces(Square.from_str('e5')) is None
    assert board.opponent_pieces(Square.from_str('e2')) == Board.PAWN
    assert board.opponent_pieces(Square.from_str('e7')) is None
    assert board.opponent_pieces(Square.from_str('e5')) is None


def test_board_iter_pieces(basic_fens):
    for fen, *_ in basic_fens:
        board = Board(fen)
        ret = set(board.iter_pieces(Board.WHITE))
        ref = set(
            (Square(File(f), Rank(r)), board[Square(File(f), Rank(r))][0])
            for f in range(8) for r in range(8)
            if board[Square(File(f), Rank(r))] is not None and board[Square(File(f), Rank(r))][1] == Board.WHITE
        )
        assert ret == ref


def test_board_move(basic_fens):
    for (start_fen, mv, *_), (end_fen, *_) in zip(basic_fens[:-1], basic_fens[1:]):
        if mv:
            board = Board(start_fen)
            board.move(Move.from_str(mv))
            assert board.fen() == Board(end_fen).fen()


def test_board_undo_move(basic_fens):
    for (start_fen, mv, *_), (end_fen, *_) in zip(basic_fens[:-1], basic_fens[1:]):
        if mv:
            board = Board(start_fen)
            origin_fen = board.fen()

            with board.do_move(Move.from_str(mv)):
                assert board.fen() == Board(end_fen).fen()

            assert board.fen() == origin_fen
