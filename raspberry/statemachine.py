import logging

import chess.engine
import serial

import States.choicestate
import States.endstate
import States.movestate
import States.stablestate
import cmd_file
import displayfile
from ledboard import ledboard
from movehandlerfile import MOVEHANDLER


class Machine:
    def __init__(self,
                 engine: chess.engine.SimpleEngine,
                 display: displayfile.DISPLAY,
                 IO_Board: serial.serialposix.Serial,
                 startposition: str = None):

        if startposition is None:
            self.board: chess.Board = chess.Board()
        else:
            self.board: chess.Board = chess.Board(startposition)
        self.engine = engine
        self.display = display
        self.Movehandler = MOVEHANDLER()
        self.leds = ledboard(IO_Board)
        self.con = IO_Board

        self.choicestate = States.choicestate.Choicestate(self)
        self.stablestate = States.stablestate.stablestate(self)
        self.movestate = States.movestate.movestate(self)
        self.endstate = States.endstate.endstate(self)

        self.comcoluour: chess.Color = None;
        self.skilllevel = 20

        self.exitflag = False

        self.State = None
        self.choicestate.activate()

    @property
    def boardstrlist(self)-> list[str]:
        """Returns a list of all currently occupied Spaces on the Board"""
        return [chess.square_name(i) for i in self.board.piece_map()]


    def disp_update(self):
        """Update the Board on the Display to reflect the Board"""
        self.display.set_fen(self.board)

    def exec_command(self,command):
        """Execute the given Command"""

        if not isinstance(command, cmd_file.BaseCommand):
            logging.warning(f"The following is not a Command {command}. Ignoring it.")
            return

        logging.info(f"CMD: {command}")

        match type(command):
            case cmd_file.Stop:
                print("stopping")
                self.State.stop()
                self.exitflag = True

            case cmd_file.Takeback:
                self.State.takeback()

            case cmd_file.Stabilise:
                self.State.Stabilise()

            case None:
                pass

            case x:
                logging.info("Command with no prefab. Taking it to the State.")
                self.State.command_handle(command)

    # TODO denhier Erneuern
    @property
    def poslist(self):
        rlist = []

        self.con.write(b"b\n")

        while True:
            if self.con.in_waiting != 0:
                data = self.con.readline().decode("utf-8").strip()

                if data[0] == "v":
                    if data == "v":
                        return []
                    else:
                        a = data[1:-1].split(";")

                        logging.debug(f"Position: {a}")
                        return a

                logging.warning(f"Unexpected Answer to b Command: {data}")