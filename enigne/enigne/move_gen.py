from typing import Iterable

from .board import Board, Move, Rank, Square


def _pawn_moves(board: Board, square: Square) -> Iterable[Move]:
    # Pawn ordinal moves
    ahead = 1 if board.turn == Board.WHITE else -1
    end = square + (0, ahead)
    if board[end] is None:
        if square.rank != board.rel_rank(Rank(6)):
            yield Move(square, end)
            if square.rank == board.rel_rank(Rank(1)):
                end = square + (0, 2 * ahead)
                if board[end] is None:
                    yield Move(square, end)
        else:
            # Promotions
            for pr_pc in {Board.KNIGHT, Board.BISHOP, Board.ROOK, Board.QUEEN}:
                yield Move(square, end, pr_pc)

    # Pawn Captures
    for df in {-1, 1}:
        end = square + (df, ahead)
        if end.is_valid() and board.opponent_pieces(end) is not None:
            if square.rank != board.rel_rank(Rank(6)):
                yield Move(square, end)
            else:
                # Promotion capture
                for pr_pc in {Board.KNIGHT, Board.BISHOP, Board.ROOK, Board.QUEEN}:
                    yield Move(square, end, pr_pc)

    # Enpassant
    if board.enpassant is not None:
        end = board.enpassant
        for df in {-1, 1}:
            start = end + (df, -ahead)
            if board.own_pieces(start, Board.PAWN) is not None:
                yield Move(start, end)


def _leaper_moves(board: Board, square: Square, m: int, n: int) -> Iterable[Move]:
    end = square + (m, n)
    if end.is_valid() and board.own_pieces(end) is None:
        yield Move(square, square + (m, n))


def _rider_moves(board: Board, square: Square, m: int, n: int) -> Iterable[Move]:
    end = square
    for step in range(7):
        end = end + (m, n)
        if not end.is_valid() or board.own_pieces(end) is not None:
            break
        yield Move(square, end)
        if board.opponent_pieces(end) is not None:
            break


def move_gen(board: Board) -> Iterable[Move]:
    """Generates pseudo-legal moves."""
    for square, piece in board.iter_own_pieces():
        if piece == Board.PAWN:
            yield from _pawn_moves(board, square)
        elif piece == Board.KING:
            yield from (
                move
                for m in {1, 0, -1} for n in {1, 0, -1}
                for move in _leaper_moves(board, square, m, n)
                if m != 0 or n != 0
            )

            if board.has_king_castling(board.turn) \
                    and board[square + (1, 0)] is None and board[square + (2, 0)] is None:

                yield Move(square, square + (2, 0))

            if board.has_queen_castling(board.turn) and \
                    board[square + (-1, 0)] is None and board[square + (-2, 0)] is None \
                    and board[square + (-3, 0)] is None:

                yield Move(square, square + (-2, 0))

        elif piece == Board.KNIGHT:
            yield from (
                move
                for m in {-2, -1, 1, 2} for n in {-2, -1, 1, 2}
                for move in _leaper_moves(board, square, m, n)
                if abs(m) + abs(n) == 3
            )

        elif piece == Board.ROOK:
            yield from (
                move
                for m in {1, 0, -1} for n in {1, 0, -1}
                for move in _rider_moves(board, square, m, n)
                if abs(m) + abs(n) == 1
            )

        elif piece == Board.BISHOP:
            yield from (
                move
                for m in {1, -1} for n in {1, -1}
                for move in _rider_moves(board, square, m, n)
            )

        elif piece == Board.QUEEN:
            yield from (
                move
                for m in {1, 0, -1} for n in {1, 0, -1}
                for move in _rider_moves(board, square, m, n)
                if m != 0 or n != 0
            )
