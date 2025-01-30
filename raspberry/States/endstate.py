import logging
import os
from datetime import datetime

import chess

import States.basestate
from config import pngdir

import chess.pgn

# Hack for IDE Support
if False:
    from statemachine import Machine


class endstate(States.basestate.State):
    def __init__(self, machine: "Machine"):
        self.machine = machine

    def activate(self):
        logging.info("Activating endstate")

        self.machine.State = self

        if self.machine.board.is_checkmate():
            match self.machine.board.outcome().winner:
                case chess.WHITE:
                    self.machine.display.setscene("1_2:w")
                case chess.BLACK:
                    self.machine.display.setscene("1_2:b")
        else:
            self.machine.display.setscene("1_2:p")

        filename = "chessgame-" + datetime.now().strftime("%Y-%m-%d-%H-%M") + ".pgn"

        com_filename = os.path.join(pngdir, filename)

        game = chess.pgn.Game.from_board(self.machine.board)

        game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")

        if self.machine.comcoluour == chess.BLACK:
            game.headers["Black"] = "Stockfish"

        if self.machine.comcoluour == chess.WHITE:
            game.headers["White"] = "Stockfish"

        with open(com_filename, "w") as f:
            exporter = chess.pgn.FileExporter(f)
            game.accept(exporter)

        print("Saved game at:", com_filename)
