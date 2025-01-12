import os
import random
from datetime import datetime
from logging import warning

import chess.engine
import chess.pgn
import serial

import cmd_file
import movehandlerfile
import startpos
from config import path, port, dispport
#from config import pngdir
from displayfile import DISPLAY
from startpos import waitforpos
from toolbox import boardtopos

now = datetime.now()
exitflag = False

arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
arduino.reset_input_buffer()

MH = movehandlerfile.MOVEHANDLER()
CH = cmd_file.CMD_HANDLER()

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(path)
display = DISPLAY(dispport)


PlayerColor = display.Waitforgamemode()

print(PlayerColor)

if PlayerColor == "Random":
    PlayerColor = random.choice(["white", "black"])

display.setscene("1_1")

display.Addline("Waiting for Startposition")

print("Hey")

startpos.waitforstartpos(arduino, CH)

print("ho")

display.Clearlines()

if PlayerColor == "black":
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    print(board)
    print("---")
    display.Addline("COM Move: " + result.move.uci())
    waitforpos(arduino, boardtopos(board), CH, chess.square_name(result.move.to_square), )

while True:

    # sleep(0.01)
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
                        display.Addline("Your Move:" + sMove)

                        if board.is_game_over():
                            break

                        if PlayerColor != "both":
                            result = engine.play(board, chess.engine.Limit(time=0.1))
                            board.push(result.move)
                            print(board)
                            print("---")
                            display.Addline("COM Move: " + result.move.uci())

                            waitforpos(arduino, boardtopos(board), CH, chess.square_name(result.move.to_square), )
                            if board.is_game_over():
                                break

                        else:
                            print(board)
                            print("---")
                            waitforpos(arduino, boardtopos(board), CH)

                else:
                    warning("invalid move")
                    waitforpos(arduino, boardtopos(board), CH)

            case _:
                warning("unkown Beginning: " + strdata[0])

    activecmdlist = []

    if CH.cmd_ready():
        # print("CMD")
        activecmdlist.append(CH.get_cmd())

    if display.button_Cmd_ready():
        activecmdlist.append(display.get_button_Cmc())

    while len(activecmdlist) != 0:
        match activecmdlist.pop():
            case "stop":
                print("stopping")
                exitflag = True

            case "takeback":
                if PlayerColor != "both":
                    board.pop()

                bt = board.pop()
                print(f"Deletet Move {bt}. Current Board State:")
                print(board)
                waitforpos(arduino, boardtopos(board),
                           CH)

            case "stable":
                display.Addline("Stabilising")
                print("How it should Look:")
                print(board)

                waitforpos(arduino, boardtopos(board), )
                MH.clear()

                display.Removeline()
                print("now we are good!")

            case _:
                warning("Unknown Command. How did it get to main?")


    if exitflag:
        break


CH.cmd_close()

"""

i = input("Export Game?")

if i == "y" or i == "yes":
    filename = "chessgame-" + now.strftime("%Y-%m-%d-%H-%M") + ".pgn"

    com_filename = os.path.join(pngdir, filename)

    game = chess.pgn.Game.from_board(board)

    with open(com_filename, "w") as f:
        exporter = chess.pgn.FileExporter(f)
        game.accept(exporter)

    print("Saved game at:", com_filename)
    
"""

engine.close()
display.close()
