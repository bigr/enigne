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
