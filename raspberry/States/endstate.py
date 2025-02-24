import logging
import os
from datetime import datetime

import chess

import States.basestate
import cmd_file
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
                    self.machine.display.setscene("end:w")
                case chess.BLACK:
                    self.machine.display.setscene("end:b")
        else:
            self.machine.display.setscene("end:p")

        filename = "chessgame-" + datetime.now().strftime("%Y-%m-%d-%H-%M") + ".pgn"

        com_filename = os.path.join(pngdir, filename)

        game = chess.pgn.Game.from_board(self.machine.board)

        game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")

        if self.machine.comcoluour == chess.BLACK:
            game.headers["Black"] = f"Stockfish (Level {self.machine.skilllevel})"

        if self.machine.comcoluour == chess.WHITE:
            game.headers["White"] = f"Stockfish (Level {self.machine.skilllevel})"

        with open(com_filename, "w") as f:
            exporter = chess.pgn.FileExporter(f)
            game.accept(exporter)

        print("Saved game at:", com_filename)

    def command_handle(self,command):
        if isinstance(command,cmd_file.Restart):
            logging.info("Restarting game")
            self.machine.board = chess.Board()
            self.machine.choicestate.activate()
        else:
            logging.warning(f"Unknown Command: {command}")
