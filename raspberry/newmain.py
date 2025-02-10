import argparse
import logging
from time import sleep

import chess.engine
import serial

import cmd_file
import statemachine
from config import dispport, path, port
from displayfile import DISPLAY

logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument("--fen", help="Start the board with the given fen Position. Defaults to Standart Start position.")
parser.add_argument("--nocli",help="Disables the CLI.(No more Commands over the Terminal)",action="store_true")

args = parser.parse_args()

IO_Board = serial.Serial(port=port, baudrate=115200, timeout=.1)
IO_Board.reset_input_buffer()

engine = chess.engine.SimpleEngine.popen_uci(path, timeout=20)

display = DISPLAY(dispport)

if not args.nocli:
    CH = cmd_file.CMD_HANDLER()

machine = statemachine.Machine(engine, display, IO_Board, startposition=args.fen)

activecmdlist = []
exitflag = False

logging.info("Beginning with loop")

while True:
    if IO_Board.in_waiting != 0:
        data = IO_Board.readline()
        strdata: str = data.decode("utf-8").strip()

        match strdata[0]:
            case "t":
                machine.State.take(strdata[1:3])
            case "p":
                machine.State.place(strdata[1:3])

    # TODO CMDhandling neu

    if not args.nocli and CH.cmd_ready():
        machine.exec_command(CH.get_cmd())

    if display.button_Cmd_ready():
        machine.exec_command(display.get_button_Cmc())

    if machine.exitflag:
        break

    sleep(0.01)

if not args.nocli:
    CH.cmd_close()
engine.close()
display.close()
