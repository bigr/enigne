from __future__ import annotations

from typing import NewType, Optional, Dict, Any

Piece = NewType('Piece', int)
Color = NewType('Color', int)
File = NewType('File', int)
Rank = NewType('Rank', int)


class Square:
    _file: File
    _rank: Rank

    def __init__(self, _file: File, _rank: Rank):
        self._file, self._rank = _file, _rank

    @property
    def file(self) -> File:
        return self._file

    @property
    def rank(self) -> Rank:
        return self._rank

    @classmethod
    def from_str(cls, square_str: str) -> Square:
        file_str, rank_str = square_str
        file = File(ord(file_str) - ord('a'))
        rank = Rank(int(rank_str) - 1)
        return cls(file, rank)

    def __eq__(self, other):
        return self.file == other.file and self.rank == other.rank

    def __repr__(self):
        return f'{self.__class__.__name__}({self.file}, {self.rank})'

    def __str__(self):
        return f"{chr(ord('a') + int(self.file))}{int(self.rank) + 1}"


class Move:
    _start: Square
    _end: Square
    _promote: Piece

    @property
    def start(self) -> Square:
        return self._start

    @property
    def end(self) -> Square:
        return self._end

    @property
    def promote(self) -> Optional[Piece]:
        return self._promote

    def __init__(self, start: Square, end: Square, promote: Optional[Piece] = None):
        self._start = start
        self._end = end
        self._promote = promote

    @classmethod
    def from_str(cls, move_str: str) -> Move:
        start, end, promote = move_str[:2], move_str[2:4], move_str[4:]
        return cls(Square.from_str(start), Square.from_str(end), Board.char_to_piece(promote) if promote else None)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.promote == other.promote

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.start)}, {repr(self.end)}, {repr(self.promote)})'

    def __str__(self):
        promote = Board.piece_to_char(self.promote, Board.BLACK) if self.promote is not None else ''
        return f"{self.start}{self.end}{promote}"


class Board:
    """Represents chess board"""

    _pieces: Dict[Any, Any]
    _turn: Color
    _castling: str
    _enpassant: Optional[Square]
    _halfmove: int
    _fullmove: int

    EMPTY, PAWN, BISHOP, KNIGHT, ROOK, QUEEN, KING = [Piece(p) for p in range(7)]
    WHITE, BLACK = Color(0), Color(1)

    @classmethod
    def char_to_piece(cls, piece_char: str) -> Piece:
        return {
            'p': cls.PAWN, 'b': cls.BISHOP, 'n': cls.KNIGHT,
            'r': cls.ROOK, 'q': cls.QUEEN, 'k': cls.KING
        }[piece_char]

    @classmethod
    def piece_to_char(cls, piece: Piece, color: Color) -> str:
        ret = ['p', 'b', 'n', 'r', 'q', 'k'][int(piece) - 1]
        return ret.upper() if color == cls.WHITE else ret

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
                    self[Square(File(file), Rank(7 - irank))] = piece, piece_color
                    file += 1

        self._turn = self.WHITE if side == 'w' else self.BLACK

        self._castling = castling
        if enpassant == '-':
            self.clear_enpassant()
        else:
            self.set_enpassant(Square.from_str(enpassant).file, self.WHITE if self._turn == self.BLACK else self.BLACK)
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
                    ss.append(self.piece_to_char(*self[Square(File(file), Rank(7 - irank))]))
            if empty:
                ss.append(str(empty))

            s.append(''.join(ss))

        return ' '.join([
            '/'.join(s),
            'w' if self._turn == self.WHITE else 'b',
            str(self._castling),
            str(self._enpassant) if self._enpassant else '-',
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

    @property
    def turn(self) -> Color:
        return self._turn

    @property
    def opponent(self) -> Color:
        return self.WHITE if self.turn == self.BLACK else self.BLACK

    def _rel_rank(self, rank: Rank) -> Rank:
        """Rank from point of the view of side to turn"""
        return Rank(7 - int(rank)) if self.turn == Board.BLACK else rank

    def clear(self):
        self._pieces = {}
        self._turn = self.WHITE
        self._castling = ''
        self.clear_enpassant()
        self._halfmove = 0
        self._fullmove = 1

    def set_enpassant(self, file: File, color: Color):
        self._enpassant = Square(file, Rank(2 if color == self.WHITE else 5))

    def clear_enpassant(self):
        self._enpassant = None

    def __setitem__(self, key, value):
        if value is None:
            if (key.rank, key.file) in self._pieces:
                del self._pieces[key.rank, key.file]
        else:
            piece, color = value
            self._pieces[key.rank, key.file] = (piece, color)

    def __getitem__(self, key):
        return self._pieces.get((key.rank, key.file), None)

    def __contains__(self, key):
        rank, file = key
        return (rank, file) in self._pieces

    def __str__(self):
        s = ["\n+-" + "--+-" * 7 + "--+\n"]
        for irank in range(8):
            s.append('| ')
            s.append(" | ".join(
                self.piece_to_char(
                    *self[Square(File(file), Rank(7 - irank))]
                ) if (7 - irank, file) in self else " "
                for file in range(8)
            ))
            s.append(" |\n+-" + "--+-" * 7 + "--+\n")
        return "".join(s)
