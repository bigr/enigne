from .board import Board


MATERIAL_SCORES = {
    Board.PAWN: 1,
    Board.BISHOP: 3,
    Board.KNIGHT: 3,
    Board.ROOK: 5,
    Board.QUEEN: 9,
    Board.KING: 0,
}


def evaluate_material(board: Board) -> float:
    return sum(MATERIAL_SCORES[piece] for _, piece in board.iter_own_pieces()) \
                - sum(MATERIAL_SCORES[piece] for _, piece in board.iter_opponent_pieces())
