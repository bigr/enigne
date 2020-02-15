from typing import NewType, Optional, Dict, Any

Piece = NewType('Piece', int)
PieceChar = NewType('PieceChar', str)
Color = NewType('Color', int)


class Board:
    """Represents chess board"""

    _pieces: Dict[Any, Any]
    _turn: Color
    _castling: str
    _enpassant: str
    _halfmove: int
    _fullmove: int

    EMPTY, PAWN, BISHOP, KNIGHT, ROOK, QUEEN, KING = [Piece(p) for p in range(7)]
    WHITE, BLACK = Color(0), Color(1)

    @classmethod
    def char_to_piece(cls, piece_char: PieceChar) -> Piece:
        return {
            'p': cls.PAWN, 'b': cls.BISHOP, 'n': cls.KNIGHT,
            'r': cls.ROOK, 'q': cls.QUEEN, 'k': cls.KING
        }[piece_char]

    @classmethod
    def piece_to_char(cls, piece: Piece, color: Color) -> PieceChar:
        ret = ['p', 'b', 'n', 'r', 'q', 'k'][int(piece) - 1]
        return PieceChar(ret.upper() if color == cls.WHITE else ret)

    def load_fen(self, fen: str):
        self.clear()
        piece_placement, side, castling, enpassant, halfmove, fullmove = fen.split(' ')
        for irank, pieces in enumerate(piece_placement.split('/')):
            file = 0
            for piece_char in pieces:
                if piece_char.isdigit():
                    file += int(piece_char)
                else:
                    piece_color = self.BLACK if piece_char.islower() else self.WHITE
                    piece = self.char_to_piece(piece_char.lower())
                    self[7 - irank, file] = piece, piece_color
                    file += 1

        self._turn = self.WHITE if side == 'w' else self.BLACK

        self._castling = castling
        self._enpassant = enpassant
        self._halfmove = int(halfmove)
        self._fullmove = int(fullmove)

    def fen(self) -> str:
        s = []
        for irank in range(8):
            ss = []
            empty = 0
            for file in range(8):
                if (7 - irank, file) not in self:
                    empty += 1
                else:
                    if empty:
                        ss.append(str(empty))
                        empty = 0
                    ss.append(self.piece_to_char(*self[7 - irank, file]))
            if empty:
                ss.append(str(empty))

            s.append(''.join(ss))

        return ' '.join([
            '/'.join(s),
            'w' if self._turn == self.WHITE else 'b',
            str(self._castling),
            str(self._enpassant),
            repr(self._halfmove),
            repr(self._fullmove),
        ])

    def __repr__(self):
        return self.fen()

    def __init__(self, fen: Optional[str] = None):
        if fen is not None:
            self.load_fen(fen)
        else:
            self.clear()

    def clear(self):
        self._pieces = {}
        self._turn = self.WHITE
        self._castling = ''
        self._enpassant = '-'

    def __setitem__(self, key, value):
        rank, file = key
        if value is None:
            if (rank, file) in self._pieces:
                del self._pieces[rank, file]
        else:
            piece, color = value
            self._pieces[rank, file] = (piece, color)

    def __getitem__(self, key):
        rank, file = key
        return self._pieces.get((rank, file), None)

    def __contains__(self, key):
        rank, file = key
        return (rank, file) in self._pieces

    def __str__(self):
        s = ["\n+-" + "--+-" * 7 + "--+\n"]
        for irank in range(8):
            s.append('| ')
            s.append(" | ".join(
                self.piece_to_char(*self[7 - irank, file]) if (7 - irank, file) in self else " " for file in range(8)
            ))
            s.append(" |\n+-" + "--+-" * 7 + "--+\n")
        return "".join(s)
