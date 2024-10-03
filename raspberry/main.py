from logging import warning

import chess
import serial

import movehandlerfile

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

MH = movehandlerfile.MOVEHANDLER()

board = chess.Board()

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
                else:
                    warning("invalid move")

        else:
            warning("unkown Beginning: " + strdata[0])
