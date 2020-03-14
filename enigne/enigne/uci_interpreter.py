from __future__ import annotations

import threading
from itertools import dropwhile, takewhile
from time import sleep
from typing import Dict, List, Set, Optional

from .board import Move
from .engine import EngineBase
from .search import PVSearchVisitor, StatsSearchVisitor, BagOfSearchVisitors


class UciSearchVisitor(BagOfSearchVisitors):
    _interpreter: Optional[UciInterpreter]
    _stats: StatsSearchVisitor
    _pv: PVSearchVisitor

    def __init__(self, interpreter: UciInterpreter, parent: Optional[UciSearchVisitor] = None):
        if not parent:
            self._stats = StatsSearchVisitor()
            self._pv = PVSearchVisitor()
            visitors = {'pv': self._pv, 'stats': self._stats}
        else:
            visitors = parent._visitors
        super().__init__(visitors, parent=parent)
        if parent:
            self._stats = self._visitors['stats']
            self._pv = self._visitors['pv']
        self._interpreter = interpreter

    def _create_child(self) -> UciSearchVisitor:
        return UciSearchVisitor(self._interpreter, parent=self)

    @property
    def stats(self) -> StatsSearchVisitor:
        return self._stats

    @property
    def pv(self) -> PVSearchVisitor:
        return self._pv

    def current_move(self, move: Move) -> None:
        super().current_move(move)
        if not self._parent:
            self._interpreter.write('info', currmove=move)

    def new_best_move(self, score: float, is_principal_variation=False) -> None:
        super().new_best_move(score, is_principal_variation)
        if not self._parent and is_principal_variation:
            self._interpreter.write(
                'info',
                depth=len(self.pv.pv),
                score=f'cp {int(score * 100)}',
                nodes=self.stats.nodes,
                time=int(1000 * self.stats.duration),
                pv=' '.join([str(m) for m in self.pv.pv])
            )


class UciInterpreter:
    WAITING_STEP = 0.005

    _engine: EngineBase
    _search_visitor: UciSearchVisitor
    _search_monitor_thread: Optional[threading.Thread]

    def __init__(self, engine: EngineBase):
        self._output_io = None
        self._search_visitor = UciSearchVisitor(self)
        self._engine = engine
        self._engine.set_search_visitor(self._search_visitor)
        self._search_monitor_thread = None

    @property
    def search_visitor(self) -> UciSearchVisitor:
        return self._search_visitor

    def write(self, *args, **kwargs):
        msg = []
        if args:
            msg.append(' '.join(args))
        if kwargs:
            msg.append(' '.join(f'{k} {v}' for k, v in kwargs.items()))

        msg = ' '.join(msg)

        self._output_io.write(f'{msg}\n')
        self._output_io.flush()

    def search_log_start(self, depth: int, selective_depth: Optional[int] = None, nodes: Optional[int] = None) -> None:
        self._output_io.write(f'info depth {depth}')
        if selective_depth is not None:
            self._output_io.write(f' seldepth {selective_depth}')
        if nodes is not None:
            self._output_io.write(f' nodes {nodes}')

        self._output_io.write('\n')
        self._output_io.flush()

    @property
    def engine(self):
        return self._engine

    def run(self, input_io, output_io):
        self._output_io = output_io
        for line in iter(input_io.readline, ''):
            line = line.strip()
            if line == 'quit':
                self.engine.terminate_search()
                break
            response = self._run_cmd(line)

            if response:
                output_io.write(f"{response}\n")
                output_io.flush()

        self.engine.quit()

        if self._search_monitor_thread:
            self._search_monitor_thread.join()

        self._output_io = None

    def _run_cmd(self, line: str) -> str:
        cmd, *args = line.split()
        cmd_func = getattr(self, cmd, None)
        if cmd_func:
            response = cmd_func(*args)
        else:
            response = [f'Unknown command: {line}']

        return "\n".join(response)

    def uci(self):
        info = self.engine.info()
        return [
            f"id name {info.get('name','Unknown')}",
            f"id author {info.get('author','Unknown')}",
            "uciok",
        ]

    def isready(self):
        while self.engine.search_in_progress:
            sleep(self.WAITING_STEP)
        return ['readyok']

    def ucinewgame(self):
        self.engine.new_game()
        return []

    def position(self, *args):
        cmds = self.parse_command_args({'position', 'moves'}, *(['position'] + list(args)))
        fen, moves = None, None
        if cmds['position']:
            fen = \
                'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' \
                if cmds['position'][0] == 'startpos' \
                else " ".join(cmds['position'])
        if 'moves' in cmds:
            moves = [Move.from_str(move) for move in cmds['moves']]

        self.engine.modify_position(fen=fen, moves=moves)
        return []

    def stop(self):
        self.engine.terminate_search()
        return []

    def go(self, *args):
        commands = {
            'searchmoves', 'ponder', 'wtime', 'btime', 'winc', 'binc', 'movestogo',
            'depth', 'nodes', 'mate', 'movetime', 'infinite'
        }
        cmds = self.parse_command_args(commands, *args)

        def _read_arg(cmd: str) -> Optional[int]:
            return int(cmds[cmd][0]) if cmd in cmds else None

        if 'wtime' in cmds:
            self.engine.white_time_left = _read_arg('wtime') * 0.001
        if 'btime' in cmds:
            self.engine.black_time_left = _read_arg('btime') * 0.001
        if 'movestogo' in cmds:
            self.engine.moves_left = _read_arg('movestogo')
        if 'winc' in cmds:
            self.engine.white_time_inc = _read_arg('winc') * 0.001
        if 'binc' in cmds:
            self.engine.black_time_inc = _read_arg('binc') * 0.001

        filter_moves = [Move.from_str(move) for move in
                        cmds['searchmoves'][0].split()] if 'searchmoves' in cmds else None

        if 'mate' in cmds:
            self.engine.search_mate(
                depth=_read_arg('mate'),
                nodes=_read_arg('nodes'),
                filter_moves=filter_moves,
                timeout=_read_arg('movetime') * 0.001 if 'movetime' in cmds else None,
                blocking=False,
            )
        else:
            self.engine.search(
                depth=_read_arg('depth'),
                nodes=_read_arg('nodes'),
                filter_moves=filter_moves,
                timeout=_read_arg('movetime') * 0.001 if 'movetime' in cmds else None,
                blocking=False,
            )

        def monitor_search(interpreter: UciInterpreter):
            stats = interpreter.search_visitor.stats
            pv = interpreter.search_visitor.pv
            i = 0
            while not interpreter.engine.search_done:
                i = (i + 1) % int(1 / interpreter.WAITING_STEP)
                sleep(interpreter.WAITING_STEP)
                if i == 0:
                    self.write('info', npc=int(stats.nodes / stats.duration), nodes=stats.nodes)

            self.write('info', npc=int(stats.nodes / stats.duration), nodes=stats.nodes)
            self.write(bestmove=pv.best_move)

        # if self._search_monitor_thread:
        #     self._search_monitor_thread.join(timeout=1)

        self._search_monitor_thread = threading.Thread(target=monitor_search, args=(self, ))
        self._search_monitor_thread.start()

        return []

    @staticmethod
    def parse_command_args(commands: Set[str], *args) -> Dict[str, List[str]]:
        ret = {}
        for cmd in commands:
            if cmd not in args:
                continue
            cmd_args = list(dropwhile(lambda x: x != cmd, args))[1:]
            cmd_args = list(takewhile(lambda x: x not in commands, cmd_args))
            ret[cmd] = cmd_args
        return ret
