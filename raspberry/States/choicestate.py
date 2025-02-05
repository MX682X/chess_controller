import logging
from random import choice

import chess

import States.basestate

# Hack for IDE Support
if False:
    from statemachine import Machine


class Choicestate(States.basestate.State):
    def __init__(self, machine: "Machine"):
        self.machine = machine

    def activate(self):
        logging.info("Activating choicestate")

        self.machine.State = self
        self.machine.display.setscene("Choice")

    def cblack(self):
        self.machine.comcoluour = chess.WHITE

        self.machine.display.setscene("Game")
        self.machine.display.Addline("Waiting for Startposition")

        self.machine.stablestate.activate()

    def cwhite(self):
        self.machine.comcoluour = chess.BLACK

        self.machine.display.setscene("Game")
        self.machine.display.Addline("Waiting for Startposition")

        self.machine.stablestate.activate()

    def crand(self):
        if choice([True, False]):
            self.cblack()
        else:
            self.cwhite()
