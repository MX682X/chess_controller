import logging
from typing import TYPE_CHECKING

import chess

# Hack for IDE Support
if False:
    from statemachine import Machine


class endstate:
    def __init__(self, machine: "Machine"):
        self.machine = machine

    def activate(self):
        logging.info("Activating endstate")

        self.machine.State = self

        if self.machine.board.is_checkmate():
            match self.machine.board.outcome().winner:
                case chess.WHITE:
                    self.machine.display.setscene("S1_2:w")
                case chess.BLACK:
                    self.machine.display.setscene("S1_2:b")
        else:
            self.machine.display.setscene("S1_2:p")

    def place(self, pos):
        pass

    def take(self, pos):
        pass

    def stop(self):
        pass

    def takeback(self):
        pass

    def Stabilise(self):
        pass