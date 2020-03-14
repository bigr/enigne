import threading
import time
from io import StringIO
from itertools import dropwhile
from typing import Dict, Optional, Iterable, Union

import pytest

from enigne.board import Move, Board
from enigne.engine import EngineBase, Engine
from enigne.uci_interpreter import UciInterpreter, UciSearchVisitor


class EngineMockUp(EngineBase):
    _search_done: Optional[Move]
    _search_visitor: UciSearchVisitor

    def __init__(self):
        super().__init__()
        self._first_call = None
        self.new_game_called = False
        self.fen = None
        self._search_thread = None
        self._terminate_search = False
        self._search_done = None

    def info(self) -> Dict[str, str]:
        return {
            'author': 'AB CD',
            'name': 'XY 1.5',
            'some': 'other',
        }

    @property
    def is_search_terminating(self) -> bool:
        return False

    @property
    def search_done(self) -> Optional[Move]:
        return self._search_done

    @property
    def search_in_progress(self) -> bool:
        return not self._search_done and self._search_thread

    def new_game(self) -> None:
        self.new_game_called = True

    def modify_position(self, fen: Optional[str] = None, moves: Optional[Iterable[Move]] = None) -> None:
        if not moves:
            self.fen = fen
        else:
            if not fen:
                fen = self.fen
            board = Board(fen)
            for move in moves:
                board.move(move)
            self.fen = board.fen()

    def search(self, depth: Optional[int] = None, nodes: Optional[int] = None,
               filter_moves: Optional[Iterable[Move]] = None, timeout: Optional[float] = None,
               blocking: bool = True) -> Union[None, Move]:

        assert depth == 1

        def do_search():
            visitor = self._search_visitor
            mvs_w = [Move.from_str(mv) for mv in ['a2a4', 'b2b4', 'c2c4', 'd2d4', 'e2e4', 'f2f4', 'g2g4', 'h2h4']]
            mvs_b = [Move.from_str(mv) for mv in ['a7a5', 'b7b5', 'c7c5', 'd7d5', 'e7e5', 'f7f5', 'g7g5', 'h7h5']]
            with visitor:
                for mv in mvs_w:
                    visitor.current_move(mv)
                    with visitor.child() as child_visitor:
                        for mv2 in mvs_b:
                            child_visitor.current_move(mv2)
                            time.sleep(0.005)

                            if str(mv) == 'e2e4' and str(mv2) == 'e7e5':
                                child_visitor.new_best_move(10, is_principal_variation=True)

                            if self._terminate_search:
                                break

                    if str(mv) == 'e2e4' or not visitor.pv.best_move:
                        visitor.new_best_move(10, is_principal_variation=True)

                    if self._terminate_search:
                        break
                assert visitor.pv.best_move
                self._search_done = visitor.pv.best_move

        self._search_thread = threading.Thread(target=do_search, args=())
        self._terminate_search = False
        self._search_thread.start()
        return None

    def search_mate(self, depth: Optional[int] = None, nodes: Optional[int] = None,
                    filter_moves: Optional[Iterable[Move]] = None, timeout: Optional[float] = None,
                    blocking: bool = False) -> Union[None, Move]:

        pass

    def terminate_search(self):
        self._terminate_search = True

    def quit(self):
        if self._search_thread:
            self.terminate_search()
            self._search_thread.join()
            assert self.search_done


@pytest.fixture
def uci_interpreter():
    return UciInterpreter(EngineMockUp())


@pytest.fixture
def uci_interpreter_no_mockup():
    return UciInterpreter(Engine())


@pytest.mark.parametrize('commands, args, expected', [
    ({'a', 'b'}, 'a 1 2 b 3'.split(), {'a': ['1', '2'], 'b': ['3']}),
    ({'a', 'b'}, 'a b'.split(), {'a': [], 'b': []}),
    ({'test1', 'test2'}, 'test2 abc test1 efg abc'.split(), {'test1': ['efg', 'abc'], 'test2': ['abc']}),

])
def test_parse_cmd_args(uci_interpreter, commands, args, expected):
    assert uci_interpreter.parse_command_args(commands, *args) == expected


def test_go(uci_interpreter):
    fin = StringIO('\n'.join(['uci', 'go depth 1', 'isready', '']))
    fout = StringIO()

    start = time.perf_counter()
    uci_interpreter.run(fin, fout)
    duration = time.perf_counter() - start

    assert 64 * 0.005 + 0.05 + UciInterpreter.WAITING_STEP > duration >= 64 * 0.005

    output = fout.getvalue().split('\n')
    output = list(dropwhile(lambda x: not x.startswith('bestmove'), output))[0]
    assert output == 'bestmove e2e4'


def test_go_no_mockup(uci_interpreter_no_mockup):
    fin = StringIO('\n'.join(['uci', 'position startpos', 'go depth 2', 'isready', '']))
    fout = StringIO()
    uci_interpreter_no_mockup.run(fin, fout)
    output = fout.getvalue().split('\n')
    output = list(dropwhile(lambda x: not x.startswith('bestmove'), output))[0]
    assert output in {
        f'bestmove {mv}' for mv in
            {
                'a2a3', 'b2b3', 'c2c3', 'd2d3', 'e2e3', 'f2f3', 'g2g3', 'h2h3',
                'a2a4', 'b2b4', 'c2c4', 'd2d4', 'e2e4', 'f2f4', 'g2g4', 'h2h4',
                'b1a3', 'b1c3', 'g1f3', 'g1h3'
            }
    }


def test_stop(uci_interpreter):
    fin = StringIO('\n'.join(['uci', 'go depth 1', 'stop', '']))
    fout = StringIO()

    start = time.perf_counter()
    uci_interpreter.run(fin, fout)
    duration = time.perf_counter() - start
    assert 0.0051 + UciInterpreter.WAITING_STEP > duration


def test_uci(uci_interpreter):
    fin = StringIO("uci\n")
    fout = StringIO()

    uci_interpreter.run(fin, fout)

    assert fout.getvalue().split('\n') == ['id name XY 1.5', 'id author AB CD', 'uciok', '']


def test_isready(uci_interpreter):
    fin = StringIO('\n'.join(['uci', 'isready', '']))
    fout = StringIO()

    start = time.perf_counter()
    uci_interpreter.run(fin, fout)
    duration = time.perf_counter() - start
    assert 0.1 > duration

    output = fout.getvalue().split('\n')
    output = list(dropwhile(lambda x: x != 'uciok', output))[1:]

    assert output == ['readyok', '']


def test_ucinewgame(uci_interpreter):
    fin = StringIO('\n'.join(['uci', 'ucinewgame', '']))
    fout = StringIO()
    uci_interpreter.run(fin, fout)
    assert uci_interpreter.engine.new_game_called


@pytest.mark.parametrize('position_cmds, final_fen', [
    (['startpos'], 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'),
    (['startpos moves e2e4 c7c5'], 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2'),
    (['r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1'], 'r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1'),
    (['r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1 moves e1g1 e8c8'], '2kr3r/8/8/8/8/8/8/R4RK1 w - - 2 2'),
    (['startpos', 'moves e2e4 c7c5'], 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2'),
])
def test_position(uci_interpreter, position_cmds, final_fen):
    fin = StringIO('\n'.join(['uci', 'ucinewgame'] + [f'position {cmd}' for cmd in position_cmds] + ['', ]))
    fout = StringIO()
    uci_interpreter.run(fin, fout)
    assert uci_interpreter.engine.fen == final_fen


@pytest.mark.parametrize('cmds, output', [
    (['uci', 'isready', ''], ['uciok', 'readyok'])
])
def test_enigne_script(cmds, output, script_runner):
    ret = script_runner.run('enigne', stdin=StringIO('\n'.join(cmds)))
    assert ret.success
    assert ret.stdout.split('\n')[-len(output) - 1:-1] == output
    assert ret.stderr == ''
