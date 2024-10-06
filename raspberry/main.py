from logging import warning

import chess.engine
import serial

import movehandlerfile
import startpos
from startpos import waitforpos
from toolbox import boardtopos

from config import path,port

arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)

startpos.waitforstartpos(arduino)

MH = movehandlerfile.MOVEHANDLER()

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(path)

while True:
    if arduino.in_waiting != 0:
        data = arduino.readline()
        strdata = data.decode("utf-8").strip()
        # print(strdata)
        if strdata[0] == "t":
            MH.addtake(strdata[1:3])
            
        elif strdata[0] == "p":
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
                    waitforpos(arduino, boardtopos(board),chess.square_name(result.move.to_square))

                else:
                    warning("invalid move")
                    waitforpos(arduino,boardtopos(board))

        else:
            warning("unkown Beginning: " + strdata[0])
