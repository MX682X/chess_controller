import logging
from random import choice

import chess

# Hack for IDE Support
if False:
    from statemachine import Machine


class Choicestate:
    def __init__(self, machine: "Machine"):
        self.machine = machine

    def activate(self):
        logging.info("Activating choicestate")

        self.machine.State = self
        self.machine.display.setscene("1_0")

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

    def cblack(self):
        self.machine.COMstart = True
        self.machine.board = chess.Board()

        self.machine.display.setscene("1_1")
        self.machine.display.Addline("Waiting for Startposition")

        self.machine.stablestate.activate()

    def cwhite(self):
        self.machine.board = chess.Board()

        self.machine.display.setscene("1_1")
        self.machine.display.Addline("Waiting for Startposition")

        self.machine.stablestate.activate()

    def crand(self):
        if choice([True, False]):
            self.cblack()
        else:
            self.cwhite()
