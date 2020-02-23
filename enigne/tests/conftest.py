import pytest


@pytest.fixture
def basic_fens():
    return [
        # Initial position
        ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'e2e4', None),
        ('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1', 'c7c5', None),
        ('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2', 'g1f3', None),
        ('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2', 'g7g6', None),
        ('rnbqkbnr/pp1ppp1p/6p1/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3', None, None),
        # Some openings
        ('rnbqk2r/ppp1ppbp/3p1np1/8/2PP4/2N2NP1/PP2PP1P/R1BQKB1R b KQkq - 1 5', None, None),
        ('rnbqkb1r/ppp1pppp/5n2/3p2B1/3P4/2N5/PPP1PPPP/R2QKBNR w KQkq - 4 3', 'g5f6', None),
        ('rnbqkb1r/ppp1pppp/5B2/3p4/3P4/2N5/PPP1PPPP/R2QKBNR b KQkq - 0 3', None, None),
        # Castling
        ('r3k2r/8/8/8/8/8/8/R3K2R w - - 0 1', None, None),
        ('r3k2r/8/8/8/8/8/8/R3K2R w K - 0 1', None, None),
        ('r3k2r/8/8/8/8/8/8/R3K2R w Q - 0 1', None, None),
        ('r3k2r/8/8/8/8/8/8/R3K2R w KQ - 0 1', None, None),

        ('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1', 'e1g1', None),
        ('r3k2r/8/8/8/8/8/8/R4RK1 b kq - 1 1', 'e8c8', None),
        ('2kr3r/8/8/8/8/8/8/R4RK1 w - - 2 2', None, None),

        ('r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1', 'e8g8', None),
        ('r4rk1/8/8/8/8/8/8/R3K2R w KQ - 1 2', 'e1c1', None),
        ('r4rk1/8/8/8/8/8/8/2KR3R b - - 2 2', None, None),

        ('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1', 'e1d1', None),
        ('r3k2r/8/8/8/8/8/8/R2K3R b kq - 1 1', 'e8f8', None),
        ('r4k1r/8/8/8/8/8/8/R2K3R w - - 2 2', None, None),

        ('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1', 'a1a2', None),
        ('r3k2r/8/8/8/8/8/R7/4K2R b Kkq - 1 1', 'h8g8', None),
        ('r3k1r1/8/8/8/8/8/R7/4K2R w Kq - 2 2', 'h1g1', None),
        ('r3k1r1/8/8/8/8/8/R7/4K1R1 b q - 3 2', 'a8d8', None),
        ('3rk1r1/8/8/8/8/8/R7/4K1R1 w - - 4 3', None, None),

        ('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1', 'h1h8', None),
        ('r3k2R/8/8/8/8/8/8/R3K3 b Qq - 0 1', None, None),

        ('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1', 'a1a8', None),
        ('R3k2r/8/8/8/8/8/8/4K2R b Kk - 0 1', None, None),

        ('r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1', 'h8h1', None),
        ('r3k3/8/8/8/8/8/8/R3K2r w Qq - 0 2', None, None),

        ('r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1', 'a8a1', None),
        ('4k2r/8/8/8/8/8/8/r3K2R w Kk - 0 2', None, None),

        ('r3k2r/8/8/8/8/8/8/R3K2R b kq - 0 1', None, None),
        ('r3k2r/8/8/8/8/8/8/R3K2R b q - 0 1', None, None),
        ('r3k2r/8/8/8/8/8/8/R3K2R b k - 0 1', None, None),
        ('r3k2r/8/8/8/8/8/8/R3K2R b - - 0 1', None, None),
        # Enpassant
        ('4k3/8/8/3Pp3/8/8/8/4K3 w - e6 0 1', 'd5e6', None),
        ('4k3/8/4P3/8/8/8/8/4K3 b - - 0 1', None, None),
        ('4k3/8/8/8/3pP3/8/8/4K3 b - e3 0 1', 'd4e3', None),
        ('4k3/8/8/8/8/4p3/8/4K3 w - - 0 2', None, None),
        # Promote moves
        ('4k3/1P6/8/8/8/8/8/4K3 w - - 0 1', 'b7b8q', None),
        ('1Q2k3/8/8/8/8/8/8/4K3 b - - 0 1', None, None),
        ('4k3/1P6/8/8/8/8/8/4K3 w - - 0 1', 'b7b8r', None),
        ('1R2k3/8/8/8/8/8/8/4K3 b - - 0 1', None, None),
        ('4k3/1P6/8/8/8/8/8/4K3 w - - 0 1', 'b7b8n', None),
        ('1N2k3/8/8/8/8/8/8/4K3 b - - 0 1', None, None),
        ('4k3/8/8/8/8/8/1p6/4K3 b - - 0 1', 'b2b1q', None),
        ('4k3/8/8/8/8/8/8/1q2K3 w - - 0 2', None, None),
        ('4k3/8/8/8/8/8/1p6/4K3 b - - 0 1', 'b2b1r', None),
        ('4k3/8/8/8/8/8/8/1r2K3 w - - 0 2', None, None),
        ('4k3/8/8/8/8/8/1p6/4K3 b - - 0 1', 'b2b1b', None),
        ('4k3/8/8/8/8/8/8/1b2K3 w - - 0 2', None, None),
    ]
