import logging

import chess.engine
import serial

import States.choicestate
import States.endstate
import States.movestate
import States.stablestate
import displayfile
from ledboard import ledboard
from movehandlerfile import MOVEHANDLER


class Machine:
    def __init__(self,
                 engine: chess.engine.SimpleEngine,
                 display: displayfile.DISPLAY,
                 con: serial.serialposix.Serial,
                 startposition: str = None):

        if startposition is None:
            self.board: chess.Board = chess.Board()
        else:
            self.board: chess.Board = chess.Board(startposition)
        self.engine = engine
        self.display = display
        self.Movehandler = MOVEHANDLER()
        self.leds = ledboard(con)
        self.con = con

        self.choicestate = States.choicestate.Choicestate(self)
        self.stablestate = States.stablestate.stablestate(self)
        self.movestate = States.movestate.movestate(self)
        self.endstate = States.endstate.endstate(self)

        self.comcoluour: chess.Color = None;

        self.State = None
        self.choicestate.activate()

    @property
    def boardstrlist(self)-> list[str]:
        """Returns a list of all currently occupied Spaces on the Board"""
        return [chess.square_name(i) for i in self.board.piece_map()]


    def disp_update(self):
        """Update the Board on the Display to reflect the Board"""
        self.display.set_fen(self.board)

    # TODO denhier Erneuern
    @property
    def poslist(self):
        rlist = []

        self.con.write(b"b\n")

        while True:
            if self.con.in_waiting != 0:
                data = self.con.readline().decode("utf-8")

                if data[0] == "v":
                    if data == "v":
                        return []
                    else:
                        return data[1:-1].split(";")





