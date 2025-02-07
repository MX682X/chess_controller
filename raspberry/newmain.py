import logging
from logging import warning
from time import sleep

import chess.engine
import serial

import cmd_file
import statemachine
from config import dispport, path, port
from displayfile import DISPLAY

logging.getLogger().setLevel(logging.INFO)

arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
arduino.reset_input_buffer()

engine = chess.engine.SimpleEngine.popen_uci(path, timeout=20)
display = DISPLAY(dispport)
CH = cmd_file.CMD_HANDLER()

machine = statemachine.Machine(engine, display, arduino)

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
        # print("CMD")
        activecmdlist.append(CH.get_cmd())

    if display.button_Cmd_ready():
        logging.info("got buttoncmd")
        activecmdlist.append(display.get_button_Cmc())

    while len(activecmdlist) != 0:
        logging.info(f"CMD: {activecmdlist[-1]}")

        match activecmdlist.pop():
            case "stop":
                print("stopping")
                machine.State.stop()
                exitflag = True

            case "takeback":
                machine.State.takeback()

            case "stable":
                machine.State.Stabilise()

            case None:
                pass

            case x:
                if x.startswith("Choice:"):
                    splitcom = x.split(":")
                    machine.State.choice(splitcom[1], int(splitcom[2]))
                else:
                    warning("Unknown Command. How did it get to main?")

    if exitflag:
        break

    sleep(0.01)

CH.cmd_close()
engine.close()
display.close()
