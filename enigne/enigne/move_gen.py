from typing import Iterable, Optional

from .board import Board, Move, Rank, Square, Color


def _pawn_moves(board: Board, square: Square, color: Color) -> Iterable[Move]:
    # Pawn ordinal moves
    ahead = 1 if color == Board.WHITE else -1
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
        opponent_pieces = board.opponent_pieces(end) if color == board.turn else board.own_pieces(end)
        if end.is_valid() and opponent_pieces is not None:
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
            if start == square:
                yield Move(start, end)
                break


def _leaper_moves(board: Board, square: Square, m: int, n: int, color: Color) -> Iterable[Move]:
    end = square + (m, n)
    if end.is_valid() and board.pieces(end, color) is None:
        yield Move(square, square + (m, n))


def _rider_moves(board: Board, square: Square, m: int, n: int, color: Color) -> Iterable[Move]:
    end = square
    for step in range(7):
        end = end + (m, n)
        if not end.is_valid() or board.pieces(end, color) is not None:
            break
        yield Move(square, end)
        if board.pieces(end, Board.WHITE if color == Board.BLACK else Board.BLACK) is not None:
            break


def move_gen(board: Board, color: Optional[Color] = None) -> Iterable[Move]:
    """Generates pseudo-legal moves."""
    color = board.turn if color is None else color
    for square, piece in board.iter_pieces(color):
        if piece == Board.PAWN:
            yield from _pawn_moves(board, square, color)
        elif piece == Board.KING:
            yield from (
                move
                for m in {1, 0, -1} for n in {1, 0, -1}
                for move in _leaper_moves(board, square, m, n, color)
                if m != 0 or n != 0
            )

            if board.has_king_castling(color) \
                    and board[square + (1, 0)] is None and board[square + (2, 0)] is None:

                yield Move(square, square + (2, 0))

            if board.has_queen_castling(color) and \
                    board[square + (-1, 0)] is None and board[square + (-2, 0)] is None \
                    and board[square + (-3, 0)] is None:

                yield Move(square, square + (-2, 0))

        elif piece == Board.KNIGHT:
            yield from (
                move
                for m in {-2, -1, 1, 2} for n in {-2, -1, 1, 2}
                for move in _leaper_moves(board, square, m, n, color)
                if abs(m) + abs(n) == 3
            )

        elif piece == Board.ROOK:
            yield from (
                move
                for m in {1, 0, -1} for n in {1, 0, -1}
                for move in _rider_moves(board, square, m, n, color)
                if abs(m) + abs(n) == 1
            )

        elif piece == Board.BISHOP:
            yield from (
                move
                for m in {1, -1} for n in {1, -1}
                for move in _rider_moves(board, square, m, n, color)
            )

        elif piece == Board.QUEEN:
            yield from (
                move
                for m in {1, 0, -1} for n in {1, 0, -1}
                for move in _rider_moves(board, square, m, n, color)
                if m != 0 or n != 0
            )


def attackers(board: Board, square: Square, color: Optional[Color]) -> Iterable[Square]:
    """Returns square of pieces of given color that attacks given square."""
    yield from (move.start for move in move_gen(board, color) if move.end == square)


def is_attacked(board: Board, square: Square, color: Optional[Color]) -> bool:
    """True if square is attacked by given color."""
    return any(True for _ in attackers(board, square, color))


def in_check(board: Board):
    return is_attacked(board, board.own_king_square, board.opponent)
