import logging

import chess.engine
import serial

import States.choicestate
import States.movestate
import States.stablestate
import States.endstate

import displayfile
from ledboard import ledboard
from movehandlerfile import MOVEHANDLER


class Machine:
    def __init__(self,
                 engine: chess.engine.SimpleEngine,
                 display: displayfile.DISPLAY,
                 con: serial.serialposix.Serial):
        self.board: chess.Board = None;
        self.engine = engine
        self.display = display
        self.Movehandler = MOVEHANDLER()
        self.leds = ledboard(con)
        self.con = con

        self.COMstart = False


        self.choicestate = States.choicestate.Choicestate(self)
        self.stablestate = States.stablestate.stablestate(self)
        self.movestate = States.movestate.movestate(self)
        self.endstate = States.endstate.endstate(self)

        self.State = None
        self.choicestate.activate()

    @property
    def boardstrlist(self):
        return [chess.square_name(i) for i in self.board.piece_map()]

    # TODO denhier Erneuern
    @property
    def poslist(self):
        rlist = []

        self.con.write(b"r\n")

        while True:
            if self.con.in_waiting != 0:
                data = self.con.readline()
                strdata = data.decode("utf-8").strip()

                rlist.append(strdata)
                if len(rlist) >= 8:
                    break

        self.con.readline()
        return parseR(rlist)


def parseR(rlist: list[str]):
    placed = []
    row = 8
    for rowstr in rlist:
        # print(rowstr)

        for col in range(1, 9):
            x = rowstr[col * 2 + 1]
            match x:
                case "x":
                    placed.append(chr(col + 96) + str(row))
                case "_":
                    pass
                case y:
                    logging.warning(f"Expectet to find x or _. Found {y}")

        row -= 1
    return placed


