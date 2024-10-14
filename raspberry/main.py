from logging import warning

import chess.engine
import serial
import argparse
import board_simulator
import threading

import movehandlerfile
import startpos
from time import sleep
from startpos import waitforpos
from toolbox import boardtopos



#def run_gui(app):
#    while(1):
#        app.exec()
#        sleep(0.05)

def run(arduino, board, engine, MH):
    print ("Main Thread Started")
    startpos.waitforstartpos(arduino)
    while(1):
        sleep(0.05)
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
                            board.push_uci(sMove)
                            print(board)
                            print("---")
                            result = engine.play(board, chess.engine.Limit(time=0.1))
                            board.push(result.move)
                            print(board)
                            print("---")
                            waitforpos(arduino, boardtopos(board), chess.square_name(result.move.to_square))

                    else:
                        warning("invalid move")
                        waitforpos(arduino, boardtopos(board))

                case _:
                    warning("unkown Beginning: " + strdata[0])

def main(arduino):
    MH = movehandlerfile.MOVEHANDLER()

    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("./stockfish-executable")

    main_thread = threading.Thread(target=run, args=(arduino, board, engine, MH, ))
    main_thread.daemon = True
    main_thread.start()

    while True:
        sleep(0.1)
    

if __name__ == "__main__":
    main(serial.Serial(port="tty/ACM0/", baudrate=115200, timeout=.1))

