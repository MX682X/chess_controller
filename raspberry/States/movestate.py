import logging
from logging import warning

import chess

import States.basestate

# Hack for IDE Support
if False:
    from statemachine import Machine


class movestate(States.basestate.State):
    def __init__(self, machine: "Machine"):
        self.machine = machine

    def activate(self):
        logging.info("Activating movestate")
        if self.machine.COMstart:
            result = self.machine.engine.play(self.machine.board, chess.engine.Limit(time=0.001))
            self.machine.board.push(result.move)

            self.machine.display.Addline("COM Move: " + result.move.uci())

            self.machine.COMstart = False
            self.machine.stablestate.activate()
            return

        if self.machine.board.is_game_over():
            self.machine.endstate.activate()

        self.machine.State = self
        self.machine.Movehandler.clear()

    def take(self, pos):
        self.machine.Movehandler.addtake(pos)

    def place(self, pos):
        sMove = self.machine.Movehandler.addplace(pos)

        if sMove is None or sMove == "0000":
            return

        try:
            move = self.machine.board.find_move(
                chess.parse_square(sMove[:2]), #From
                chess.parse_square(sMove[2:])) #To
        except chess.IllegalMoveError:
            warning("invalid move")
            self.machine.stablestate.activate()
            return

        print(move)
        self.machine.board.push(move)
        self.machine.display.Addline("Your Move:" + sMove)

        if self.machine.board.is_game_over():
            self.machine.endstate.activate()
            return

        result = self.machine.engine.play(self.machine.board, chess.engine.Limit(time=0.1))
        self.machine.board.push(result.move)

        self.machine.display.Addline("COM Move: " + result.move.uci())

        self.machine.stablestate.activate(chess.square_name(result.move.to_square))

    def takeback(self):
        self.machine.board.pop()
        self.machine.board.pop()
        self.machine.stablestate.activate()

    def Stabilise(self):
        self.machine.stablestate.activate()
