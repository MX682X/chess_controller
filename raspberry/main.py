from logging import warning
from time import sleep

import chess.engine
import serial

import cmd_file
import movehandlerfile
import startpos
from config import path, port
from displayfile import DISPLAY
from startpos import waitforpos
from toolbox import boardtopos

arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)

MH = movehandlerfile.MOVEHANDLER()
CH = cmd_file.CMD_HANDLER()

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(path)
display = DISPLAY()

startpos.waitforstartpos(arduino, )

while True:
    #print("a")
    #sleep(0.01)
    if arduino.in_waiting != 0:
        data = arduino.readline()
        strdata = data.decode("utf-8").strip()
        # print(strdata)
        match strdata[0]:
            case "t":
                MH.addtake(strdata[1:3])

            case "p":
                sMove = MH.addplace(strdata[1:3])

                if sMove is not None:
                    move = chess.Move.from_uci(sMove)

                    print(move)
                    if move in board.legal_moves:
                        board.push(move)
                        print(board)
                        print("---")
                        display.set_top("Your Move: " + sMove)

                        result = engine.play(board, chess.engine.Limit(time=0.1))
                        board.push(result.move)
                        print(board)
                        print("---")
                        display.set_bottom("COM Move: " + result.move.uci())
                        waitforpos(arduino, boardtopos(board), CH, chess.square_name(result.move.to_square), )

                else:
                    warning("invalid move")
                    waitforpos(arduino, boardtopos(board), CH)

            case _:
                warning("unkown Beginning: " + strdata[0])

    if CH.cmd_ready():
        #print("CMD")
        match CH.get_cmd():
            case "stop":
                print("stopping")
                break

            case "takeback":
                board.pop()
                bt = board.pop()
                print(f"Deletet Move {bt}. Current Board State:")
                print(board)
                waitforpos(arduino, boardtopos(board),
                           CH)

            case _:
                warning("Unknown Command. How did it get to main?")
