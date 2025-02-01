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

        if self.machine.board.is_game_over():
            self.machine.endstate.activate()
            return

        #If it's the Computers Turn, let him Move
        if self.machine.board.turn == self.machine.comcoluour:
            result = self.machine.engine.play(self.machine.board, chess.engine.Limit(time=0.01))
            self.machine.board.push(result.move)

            self.machine.display.Addline("COM Move: " + result.move.uci())

            self.machine.stablestate.activate(chess.square_name(result.move.to_square))
            return

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
        self.machine.stablestate.activate()

    def takeback(self):
        #Remove the last two played moves (The Computer Move and your move and Stabilise that Positon)
        self.machine.board.pop()
        self.machine.board.pop()
        self.machine.stablestate.activate()

    def Stabilise(self):
        self.machine.stablestate.activate()
