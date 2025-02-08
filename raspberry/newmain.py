import argparse
import logging
from logging import warning
from time import sleep

import chess.engine
import serial

import cmd_file
import statemachine
from cmd_file import BaseCommand
from config import dispport, path, port
from displayfile import DISPLAY

logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument("--fen", help="Start the board with the given fen Position. Defaults to Standart Start position.")

args = parser.parse_args()

arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
arduino.reset_input_buffer()

engine = chess.engine.SimpleEngine.popen_uci(path, timeout=20)

display = DISPLAY(dispport)
CH = cmd_file.CMD_HANDLER()

machine = statemachine.Machine(engine, display, arduino, startposition=args.fen)

activecmdlist = []
exitflag = False

logging.info("Beginning with loop")

while True:
    if arduino.in_waiting != 0:
        data = arduino.readline()
        strdata: str = data.decode("utf-8").strip()

        match strdata[0]:
            case "t":
                machine.State.take(strdata[1:3])
            case "p":
                machine.State.place(strdata[1:3])

    # TODO CMDhandling neu

    if CH.cmd_ready():
        machine.exec_command(CH.get_cmd())

    if display.button_Cmd_ready():
        machine.exec_command(display.get_button_Cmc())

    if machine.exitflag:
        break

    sleep(0.01)

CH.cmd_close()
engine.close()
display.close()
