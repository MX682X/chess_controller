from logging import warning

import chess.engine
import chess.pgn

import serial
from config import path, port#, pngdir

import cmd_file
import movehandlerfile
import startpos
from displayfile import DISPLAY
from startpos import waitforpos
from toolbox import boardtopos, get_playmode

PlayerColor = get_playmode()

arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
arduino.reset_input_buffer()

MH = movehandlerfile.MOVEHANDLER()
CH = cmd_file.CMD_HANDLER()

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(path)
display = DISPLAY()

display.set_top("Startposition")
display.write()

startpos.waitforstartpos(arduino, CH)

if PlayerColor == "black":
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    print(board)
    print("---")
    display.set_bottom("COM Move: " + result.move.uci())
    display.write()
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
                        display.set_top("Your Move: " + sMove)

                        if board.is_game_over():
                            break

                        if PlayerColor != "both":
                            result = engine.play(board, chess.engine.Limit(time=0.1))
                            board.push(result.move)
                            print(board)
                            print("---")
                            display.set_bottom("COM Move: " + result.move.uci())
                            display.write()
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

    if CH.cmd_ready():
        # print("CMD")
        match CH.get_cmd():
            case "stop":
                print("stopping")
                break

            case "takeback":
                if PlayerColor != "both":
                    board.pop()

                bt = board.pop()
                print(f"Deletet Move {bt}. Current Board State:")
                print(board)
                waitforpos(arduino, boardtopos(board),
                           CH)

            case _:
                warning("Unknown Command. How did it get to main?")

CH.cmd_close()

"""

i = input("Export Game?")

if i == "y" or i == "yes":


    game = chess.pgn.Game.from_board(board)
    with open(pngdir)

"""
engine.close()
display.close()

