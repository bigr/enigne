import pytest


@pytest.fixture
def basic_fens():
    return [
        # Initial position
        ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',),
        ('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1',),
        ('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2',),
        # Some openings
        ('rnbqk2r/ppp1ppbp/3p1np1/8/2PP4/2N2NP1/PP2PP1P/R1BQKB1R b KQkq - 1 5',),
        ('rnbqkb1r/ppp1pppp/5n2/3p2B1/3P4/2N5/PPP1PPPP/R2QKBNR b KQkq - 4 3',),
        # Castling
        ('r3k2r/8/8/8/8/8/8/R3K2R w - - 0 1',),
        ('r3k2r/8/8/8/8/8/8/R3K2R w K - 0 1',),
        ('r3k2r/8/8/8/8/8/8/R3K2R w Q - 0 1',),
        ('r3k2r/8/8/8/8/8/8/R3K2R w KQ - 0 1',),
        ('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1',),
        ('r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1',),
        ('r3k2r/8/8/8/8/8/8/R3K2R b kq - 0 1',),
        ('r3k2r/8/8/8/8/8/8/R3K2R b q - 0 1',),
        ('r3k2r/8/8/8/8/8/8/R3K2R b k - 0 1',),
        ('r3k2r/8/8/8/8/8/8/R3K2R b - - 0 1',),
        # Enpassant
        ('4k3/8/8/3Pp3/8/8/8/4K3 w - e6 0 1',),
        ('4k3/8/8/8/3pP3/8/8/4K3 w - e3 0 1',),
        # Promote moves
        ('4k3/1P6/8/8/8/8/8/4K3 w - - 0 1',),
        ('4k3/8/8/8/8/8/1p6/4K3 b - - 0 1',),
    ]
