import logging

import chess

import States.basestate


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
