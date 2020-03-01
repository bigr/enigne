from __future__ import annotations

from typing import NewType, Optional, Dict, Any, Set, Tuple, Iterator

Piece = NewType('Piece', int)
Color = NewType('Color', int)
File = NewType('File', int)
Rank = NewType('Rank', int)
ColoredPiece = Tuple[Piece, Color]


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

    def is_valid(self) -> bool:
        return 0 <= self.file < 8 and 0 <= self.rank < 8

    def __eq__(self, other):
        return self.file == other.file and self.rank == other.rank

    def __repr__(self):
        return f'{self.__class__.__name__}({self.file}, {self.rank})'

    def __str__(self):
        return f"{chr(ord('a') + int(self.file))}{int(self.rank) + 1}"

    def __hash__(self):
        return self._file | (self._rank << 3)

    def __add__(self, other: Tuple[int, int]) -> Square:
        return Square(File(int(self.file) + other[0]), Rank(int(self.rank) + other[1]))


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
    _castling: Set[str]
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

    def load_fen(self, fen: str) -> None:
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

        self.clear_castling()
        if 'K' in castling:
            self.set_king_castling(self.WHITE)
        if 'k' in castling:
            self.set_king_castling(self.BLACK)
        if 'Q' in castling:
            self.set_queen_castling(self.WHITE)
        if 'q' in castling:
            self.set_queen_castling(self.BLACK)

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
            self._castling_to_str(),
            str(self._enpassant) if self._enpassant else '-',
            repr(self._halfmove),
            repr(self._fullmove),
        ])

    def __repr__(self) -> str:
        return self.fen()

    def __init__(self, fen: Optional[str] = None):
        if fen is not None:
            self.load_fen(fen)
        else:
            self.clear()

    @property
    def turn(self) -> Color:
        return self._turn

    @turn.setter
    def turn(self, value: Color) -> None:
        self._turn = value

    @property
    def opponent(self) -> Color:
        return self.WHITE if self.turn == self.BLACK else self.BLACK

    @property
    def enpassant(self) -> Optional[Square]:
        return self._enpassant

    def rel_rank(self, rank: Rank) -> Rank:
        """Rank from point of the view of side to turn"""
        return Rank(7 - int(rank)) if self.turn == Board.BLACK else rank

    def clear(self) -> None:
        self._pieces = {}
        self._turn = self.WHITE
        self.clear_castling()
        self.clear_enpassant()
        self._halfmove = 0
        self._fullmove = 1

    def set_enpassant(self, file: File, color: Color) -> None:
        self._enpassant = Square(file, Rank(2 if color == self.WHITE else 5))

    def clear_enpassant(self) -> None:
        self._enpassant = None

    def clear_castling(self) -> None:
        self._castling = set()

    def has_any_castling(self) -> bool:
        return bool(self._castling)

    def has_queen_castling(self, color: Color) -> bool:
        return ('Q' if color == self.WHITE else 'q') in self._castling

    def has_king_castling(self, color: Color) -> bool:
        return ('K' if color == self.WHITE else 'k') in self._castling

    def set_queen_castling(self, color: Color) -> None:
        self._castling.add('Q' if color == self.WHITE else 'q')

    def set_king_castling(self, color: Color) -> None:
        self._castling.add('K' if color == self.WHITE else 'k')

    def unset_queen_castling(self, color: Color) -> None:
        self._castling.remove('Q' if color == self.WHITE else 'q')

    def unset_king_castling(self, color: Color) -> None:
        self._castling.remove('K' if color == self.WHITE else 'k')

    def _castling_to_str(self) -> str:
        if not self.has_any_castling():
            return '-'
        else:
            return "".join([
                'K' if self.has_king_castling(self.WHITE) else '',
                'Q' if self.has_queen_castling(self.WHITE) else '',
                'k' if self.has_king_castling(self.BLACK) else '',
                'q' if self.has_queen_castling(self.BLACK) else '',
            ])

    def iter_pieces(self, color: Color) -> Iterator[Tuple[Square, Piece]]:
        yield from (
            (Square(File(file), Rank(rank)), pc)
            for (rank, file), (pc, cl) in self._pieces.items()
            if cl == color
        )

    def iter_own_pieces(self):
        yield from self.iter_pieces(self.turn)

    def iter_opponent_pieces(self):
        yield from self.iter_pieces(self.opponent)

    def move(self, move: Move) -> Any:
        """
        Moves pieces on the board.
        :param move:
        :return: Data needed for undoing move.
        """

        undo_info = \
            self._turn, self._enpassant, self._halfmove, self._fullmove, self._pieces.copy(), self._castling.copy()

        piece, color = self[move.start]
        captured_piece, _ = self[move.end] or (None, None)

        # Half move counter
        if piece == self.PAWN or self[move.end] is not None:
            self._halfmove = 0
        else:
            self._halfmove += 1

        # Full move counter
        if self.turn == self.BLACK:
            self._fullmove += 1

        self[move.end], self[move.start] = ((move.promote, self.turn) if move.promote else self[move.start]), None

        # Enpassant capture
        if self._enpassant and piece == self.PAWN and move.end.file == self._enpassant.file:
            if move.end.rank == self.rel_rank(Rank(5)):
                self[Square(move.end.file, self.rel_rank(Rank(4)))] = None

        # Enpassant square
        if piece == self.PAWN and abs(move.start.rank - move.end.rank) == 2:
            self.set_enpassant(move.start.file, self.turn)
        else:
            self.clear_enpassant()

        # Castling
        if piece == self.KING and abs(move.start.file - move.end.file) == 2:
            if move.end.file == File(6):
                start = Square(File(7), move.end.rank)
                end = Square(File(5), move.end.rank)
            else:
                start = Square(File(0), move.end.rank)
                end = Square(File(3), move.end.rank)

            self[end], self[start] = self[start], None

        # Castling flags
        if piece == self.KING:
            self.unset_king_castling(self.turn)
            self.unset_queen_castling(self.turn)
        if piece == self.ROOK and move.start.rank == self.rel_rank(Rank(0)):
            if move.start.file == File(0):
                self.unset_queen_castling(self.turn)
            elif move.start.file == File(7):
                self.unset_king_castling(self.turn)
        if captured_piece == self.ROOK and move.end.rank == self.rel_rank(Rank(7)):
            if move.end.file == File(0):
                self.unset_queen_castling(self.opponent)
            elif move.end.file == File(7):
                self.unset_king_castling(self.opponent)

        # Change side
        self._turn = self.opponent

        return undo_info

    def pieces(self, square: Square, filter_color: Color, filter_piece: Optional[Piece] = None) -> Optional[Piece]:
        colored_piece = self[square]
        if colored_piece is None:
            return None
        else:
            piece, color = colored_piece
            if filter_piece is not None and filter_piece != piece:
                return None
            return piece if filter_color == color else None

    def opponent_pieces(self, square: Square, filter_piece: Optional[Piece] = None) -> Optional[Piece]:
        return self.pieces(square, self.opponent, filter_piece)

    def own_pieces(self, square: Square, filter_piece: Optional[Piece] = None) -> Optional[Piece]:
        return self.pieces(square, self.turn, filter_piece)

    def __setitem__(self, key: Square, value: Optional[ColoredPiece]) -> None:
        if value is None:
            if (key.rank, key.file) in self._pieces:
                del self._pieces[key.rank, key.file]
        else:
            piece, color = value
            self._pieces[key.rank, key.file] = (piece, color)

    def __getitem__(self, key: Square) -> Optional[ColoredPiece]:
        return self._pieces.get((key.rank, key.file), None)

    def __contains__(self, key: Square) -> bool:
        rank, file = key
        return (rank, file) in self._pieces

    def __str__(self) -> str:
        s = ["\n+-" + "--+-" * 7 + "--+\n"]
        for irank in range(8):
            s.append('| ')
            s.append(" | ".join(
                self.piece_to_char(
                    *self[Square(File(file), Rank(7 - irank))]
                ) if Square(File(file), Rank(7 - irank)) in self else " "
                for file in range(8)
            ))
            s.append(" |\n+-" + "--+-" * 7 + "--+\n")
        return "".join(s)
