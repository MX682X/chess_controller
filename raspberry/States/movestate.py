import logging
from logging import warning
from typing import TYPE_CHECKING

import chess

# Hack for IDE Support
if False:
    from statemachine import Machine


class movestate:
    def __init__(self, machine: "Machine"):
        self.machine = machine

    def activate(self):
        logging.info("Activating movestate")
        if self.machine.COMstart:
            result = self.machine.engine.play(self.machine.board, chess.engine.Limit(time=0.1))
            self.machine.board.push(result.move)

            self.machine.display.Addline("COM Move: " + result.move.uci())

            self.machine.COMstart = False
            self.machine.stablestate.activate()
            return

        self.machine.State = self
        self.machine.Movehandler.clear()

    def take(self, pos):
        self.machine.Movehandler.addtake(pos)

    def place(self, pos):
        sMove = self.machine.Movehandler.addplace(pos)

        if sMove is not None:
            move = chess.Move.from_uci(sMove)

            print(move)
            if move in self.machine.board.legal_moves:
                self.machine.board.push(move)
                self.machine.display.Addline("Your Move:" + sMove)

                if self.machine.board.is_game_over():
                    self.machine.endstate.activate()
                    return

                result = self.machine.engine.play(self.machine.board, chess.engine.Limit(time=0.1))
                self.machine.board.push(result.move)

                self.machine.display.Addline("COM Move: " + result.move.uci())

                if self.machine.board.is_variant_end():
                    self.machine.endstate.activate()
                else:
                    self.machine.stablestate.activate(chess.square_name(result.move.to_square))

        else:
            warning("invalid move")
            self.machine.stablestate.activate()

    def stop(self):
        pass

    def takeback(self):
        self.machine.board.pop()
        self.machine.board.pop()
        self.machine.stablestate.activate()

    def Stabilise(self):
        self.machine.stablestate.activate()
