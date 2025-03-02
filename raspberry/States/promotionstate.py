import logging
from logging import warning

import chess

import cmd_file

import States.basestate

if False:
    from statemachine import Machine


class Promotionstate(States.basestate.State):
    def __init__(self, machine: "Machine"):
        self.machine = machine
        self.move: chess.Move = None

    def activate(self, move: chess.Move):
        if move.promotion is None:
            warning(
                "Trying to activate Promotion State but the Move is not a Promotion Move. Activating Stable State instead.")
            self.machine.stablestate.activate()
            return

        logging.info("Activating Promotion State")
        self.machine.State = self
        self.move = move
        if self.machine.board.turn == chess.WHITE:
            self.machine.display.setscene("Promotion:white")
        else:
            self.machine.display.setscene("Promotion:black")

    def command_handle(self, command):
        if not isinstance(command, cmd_file.Promotion):
            logging.warning(f"Unknown Command: {command}")
            return

        self.move.promotion = command.Piece
        self.machine.board.push(self.move)
        self.machine.display.Addline("Your Move:" + self.move.uci())
        self.machine.display.setscene("Game")
        self.machine.stablestate.activate()