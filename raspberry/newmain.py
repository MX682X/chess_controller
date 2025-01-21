from logging import warning

import chess.engine
import serial

import cmd_file
import statemachine
from config import dispport, path, port
from displayfile import DISPLAY

arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
arduino.reset_input_buffer()

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(path)
display = DISPLAY(dispport)
CH = cmd_file.CMD_HANDLER()

machine = statemachine.Machine(engine, display, arduino)

activecmdlist = []
exitflag = False

while True:
    if arduino.in_waiting != 0:
        data = arduino.readline()
        strdata: str = data.decode("utf-8").strip()

        if strdata.startswith("COM:BTN1_0:"):
            match strdata:
                case "COM:BTN1_0:CB":
                    machine.State.cblack()
                case "COM:BTN1_0:CW":
                    machine.State.cwhite()
                case "COM:BTN1_0:CR":
                    machine.State.crand()
        else:
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
        activecmdlist.append(display.get_button_Cmc())

    while len(activecmdlist) != 0:
        match activecmdlist.pop():
            case "stop":
                print("stopping")
                machine.State.stop()
                exitflag = True

            case "takeback":
                machine.State.takeback()

            case "stable":
                machine.State.Stabilise()

            case _:
                warning("Unknown Command. How did it get to main?")

    if exitflag:
        break


CH.cmd_close()
engine.close()
display.close()
