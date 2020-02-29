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

        # Basic pseude-legal moves test positions
        # Pawn
        ('8/8/8/8/8/8/4P3/8 w - - 0 1', None, {'e2e3', 'e2e4'}),
        ('8/8/8/8/8/4P3/8/8 w - - 0 1', None, {'e3e4'}),
        ('8/3p4/8/8/8/8/8/8 b - - 0 1', None, {'d7d6', 'd7d5'}),
        ('8/8/3p4/8/8/8/8/8 b - - 0 1', None, {'d6d5'}),
        ('8/8/8/3p4/4P3/8/8/8 w - - 0 1', None, {'e4d5', 'e4e5'}),
        ('8/8/8/3p4/4P3/8/8/8 b - - 0 1', None, {'d5e4', 'd5d4'}),
        ('8/8/8/4p3/4P3/8/8/8 w - - 0 1', None, set()),
        ('8/8/8/4p3/4P3/8/8/8 b - - 0 1', None, set()),
        ('8/8/8/4P3/4P3/8/8/8 w - - 0 1', None, {'e5e6'}),
        ('8/8/8/4p3/4p3/8/8/8 b - - 0 1', None, {'e4e3'}),
        ('8/8/8/8/8/4p3/4P3/8 w - - 0 1', None, set()),
        ('8/8/8/8/4p3/8/4P3/8 w - - 0 1', None, {'e2e3'}),
        ('8/4p3/4P3/8/8/8/8/8 b - - 0 1', None, set()),
        ('8/4p3/8/4P3/8/8/8/8 b - - 0 1', None, {'e7e6'}),
        ('8/8/8/8/8/4P3/4p3/8 w - - 0 1', None, {'e3e4'}),
        ('8/8/8/8/4P3/8/4P3/8 w - - 0 1', None, {'e2e3', 'e4e5'}),
        ('8/4p3/4p3/8/8/8/8/8 b - - 0 1', None, {'e6e5'}),
        ('8/4p3/8/4p3/8/8/8/8 b - - 0 1', None, {'e7e6', 'e5e4'}),
        ('8/8/8/3pp3/3PP3/8/8/8 w - - 0 1', None, {'d4e5', 'e4d5'}),
        ('8/8/8/3pp3/3PP3/8/8/8 b - - 0 1', None, {'d5e4', 'e5d4'}),
        ('8/8/8/3pP3/3Pp3/8/8/8 w - - 0 1', None, {'e5e6'}),
        ('8/8/8/3pP3/3Pp3/8/8/8 b - - 0 1', None, {'e4e3'}),
        ('8/8/8/4Pp2/8/8/8/8 w - f6 0 1', None, {'e5e6', 'e5f6'}),
        ('8/8/8/8/4Pp2/8/8/8 b - e3 0 1', None, {'f4f3', 'f4e3'}),
        ('8/8/8/4Pp2/8/8/8/8 w - - 0 1', None, {'e5e6'}),
        ('8/8/8/8/4Pp2/8/8/8 b - - 0 1', None, {'f4f3'}),
        ('8/7P/8/8/8/8/8/8 w - - 0 1', None, {'h7h8n', 'h7h8b', 'h7h8r', 'h7h8q'}),
        ('7n/7P/8/8/8/8/8/8 w - - 0 1', None, set()),
        ('8/8/8/8/8/8/p7/8 b - - 0 1', None, {'a2a1n', 'a2a1b', 'a2a1r', 'a2a1q'}),
        ('8/8/8/8/8/8/p7/B7 b - - 0 1', None, set()),
        ('6qN/7P/8/8/8/8/8/8 w - - 0 1', None, {'h7g8n', 'h7g8b', 'h7g8r', 'h7g8q', 'h8f7', 'h8g6'}),
        ('8/8/8/8/8/8/p7/rN6 b - - 0 1', None, {'a2b1n', 'a2b1b', 'a2b1r', 'a2b1q', 'a1b1'}),
        ('6qn/7P/8/8/8/8/8/8 w - - 0 1', None, {'h7g8n', 'h7g8b', 'h7g8r', 'h7g8q'}),
        ('8/8/8/8/8/8/p7/RN6 b - - 0 1', None, {'a2b1n', 'a2b1b', 'a2b1r', 'a2b1q'}),
        ('6NN/7P/8/8/8/8/8/8 w - - 0 1', None, {'g8e7', 'g8h6', 'h8f7', 'h8g6', 'g8f6'}),
        ('8/8/8/8/8/8/p7/rn6 b - - 0 1', None, {'b1d2', 'b1c3', 'b1a3'}),

        # King
        ('8/8/8/8/8/3K4/8/8 w - - 0 1', None, {'d3c2', 'd3c3', 'd3c4', 'd3d2', 'd3d4', 'd3e2', 'd3e3', 'd3e4'}),
        ('8/8/8/8/8/3k4/8/8 b - - 0 1', None, {'d3c2', 'd3c3', 'd3c4', 'd3d2', 'd3d4', 'd3e2', 'd3e3', 'd3e4'}),
        ('8/8/8/8/3P4/3K4/8/8 w - - 0 1', None, {'d3c2', 'd3c3', 'd3c4', 'd3d2', 'd3e2', 'd3e3', 'd3e4', 'd4d5'}),
        ('8/8/8/8/3p4/3k4/8/8 b - - 0 1', None, {'d3c2', 'd3c3', 'd3c4', 'd3d2', 'd3e2', 'd3e3', 'd3e4'}),
        ('8/8/8/8/3p4/3K4/8/8 w - - 0 1', None, {'d3c2', 'd3c3', 'd3c4', 'd3d2', 'd3d4', 'd3e2', 'd3e3', 'd3e4'}),
        ('8/8/8/8/3P4/3k4/8/8 b - - 0 1', None, {'d3c2', 'd3c3', 'd3c4', 'd3d2', 'd3d4', 'd3e2', 'd3e3', 'd3e4'}),

        # Knight
        ('8/8/8/8/8/3N4/8/8 w - - 0 1', None, {'d3c1', 'd3e1', 'd3b2', 'd3f2', 'd3b4', 'd3f4', 'd3c5', 'd3e5'}),
        ('8/8/8/8/8/3n4/8/8 b - - 0 1', None, {'d3c1', 'd3e1', 'd3b2', 'd3f2', 'd3b4', 'd3f4', 'd3c5', 'd3e5'}),
        ('8/8/8/2P5/8/3N4/8/8 w - - 0 1', None, {'d3c1', 'd3e1', 'd3b2', 'd3f2', 'd3b4', 'd3f4', 'd3e5', 'c5c6'}),
        ('8/8/8/2p5/8/3n4/8/8 b - - 0 1', None, {'d3c1', 'd3e1', 'd3b2', 'd3f2', 'd3b4', 'd3f4', 'd3e5', 'c5c4'}),
        ('8/8/8/2p5/8/3N4/8/8 w - - 0 1', None, {'d3c1', 'd3e1', 'd3b2', 'd3f2', 'd3b4', 'd3f4', 'd3c5', 'd3e5'}),
        ('8/8/8/2P5/8/3n4/8/8 b - - 0 1', None, {'d3c1', 'd3e1', 'd3b2', 'd3f2', 'd3b4', 'd3f4', 'd3c5', 'd3e5'}),

        # Rook
        ('8/8/8/8/8/8/1R6/8 w - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4', 'b2b5', 'b2b6', 'b2b7', 'b2b8',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
        }),
        ('8/8/8/8/8/8/1r6/8 b - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4', 'b2b5', 'b2b6', 'b2b7', 'b2b8',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
        }),
        ('8/8/8/8/1p6/8/1R6/8 w - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
        }),
        ('8/8/8/8/1P6/8/1R6/8 w - - 0 1', None, {
            'b2b1', 'b2b3', 'b4b5',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
        }),
        ('8/8/8/8/1P6/8/1r6/8 b - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
        }),
        ('8/8/8/8/1p6/8/1r6/8 b - - 0 1', None, {
            'b2b1', 'b2b3', 'b4b3',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
        }),

        # Bishop
        ('8/8/8/8/8/8/1B6/8 w - - 0 1', None, {
            'b2a1', 'b2c3', 'b2d4', 'b2e5', 'b2f6', 'b2g7', 'b2h8',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/8/8/1b6/8 b - - 0 1', None, {
            'b2a1', 'b2c3', 'b2d4', 'b2e5', 'b2f6', 'b2g7', 'b2h8',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/3p4/8/1B6/8 w - - 0 1', None, {
            'b2a1', 'b2c3', 'b2d4',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/3P4/8/1B6/8 w - - 0 1', None, {
            'b2a1', 'b2c3', 'd4d5',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/3P4/8/1b6/8 b - - 0 1', None, {
            'b2a1', 'b2c3', 'b2d4',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/3p4/8/1b6/8 b - - 0 1', None, {
            'b2a1', 'b2c3', 'd4d3',
            'b2a3', 'b2c1',
        }),

        # Queen
        ('8/8/8/8/8/8/1Q6/8 w - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4', 'b2b5', 'b2b6', 'b2b7', 'b2b8',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'b2d4', 'b2e5', 'b2f6', 'b2g7', 'b2h8',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/8/8/1q6/8 b - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4', 'b2b5', 'b2b6', 'b2b7', 'b2b8',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'b2d4', 'b2e5', 'b2f6', 'b2g7', 'b2h8',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/1p6/8/1Q6/8 w - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'b2d4', 'b2e5', 'b2f6', 'b2g7', 'b2h8',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/1P6/8/1Q6/8 w - - 0 1', None, {
            'b2b1', 'b2b3', 'b4b5',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'b2d4', 'b2e5', 'b2f6', 'b2g7', 'b2h8',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/1P6/8/1q6/8 b - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'b2d4', 'b2e5', 'b2f6', 'b2g7', 'b2h8',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/1p6/8/1q6/8 b - - 0 1', None, {
            'b2b1', 'b2b3', 'b4b3',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'b2d4', 'b2e5', 'b2f6', 'b2g7', 'b2h8',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/3p4/8/1Q6/8 w - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4', 'b2b5', 'b2b6', 'b2b7', 'b2b8',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'b2d4',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/3P4/8/1Q6/8 w - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4', 'b2b5', 'b2b6', 'b2b7', 'b2b8',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'd4d5',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/3P4/8/1q6/8 b - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4', 'b2b5', 'b2b6', 'b2b7', 'b2b8',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'b2d4',
            'b2a3', 'b2c1',
        }),
        ('8/8/8/8/3p4/8/1q6/8 b - - 0 1', None, {
            'b2b1', 'b2b3', 'b2b4', 'b2b5', 'b2b6', 'b2b7', 'b2b8',
            'b2a2', 'b2c2', 'b2d2', 'b2e2', 'b2f2', 'b2g2', 'b2h2',
            'b2a1', 'b2c3', 'd4d3',
            'b2a3', 'b2c1',
        }),
    ]
