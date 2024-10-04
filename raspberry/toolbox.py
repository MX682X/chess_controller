import logging
from logging import warning

import serial


def parseR(rlist: list[str]):
    placed = []
    row = 8
    for rowstr in rlist:
        print(rowstr)

        for col in range(1, 9):
            x = rowstr[col * 2 + 1]
            match x:
                case "x":
                    placed.append(chr(col + 96) + str(row))
                case "_":
                    pass
                case _:
                    logging.warning(f"Expectet to find x or _. Found {x}")

        row -= 1
    return placed


def getreedlist(ser: serial.serialposix.Serial):
    rlist = []

    ser.write(b"r\n")

    while True:
        if ser.in_waiting != 0:
            data = ser.readline()
            strdata = data.decode("utf-8").strip()

            rlist.append(strdata)
            if len(rlist) >= 8:
                break

    ser.readline()
    return parseR(rlist)


def led_turnon(ser: serial.serialposix.Serial, field: str):
    s = "s" + field + "\n"
    ser.write(s.encode())


def led_turnoff(ser: serial.serialposix.Serial, field: str):
    s = "k" + field + "\n"
    ser.write(s.encode())


def clrall(ser: serial.serialposix.Serial):
    for row in range(1, 9):
        for col in range(97, 97 + 8):
            led_turnoff(ser, chr(col) + str(row))

def boardtopos(b):
    s = str(b).split("\n")
    res = []

    row = 8

    for r in s:
        for collum in range(8):
            match r[collum*2]:
                case " ":
                    warning("did not expect   ")
                case ".":
                    pass


                case _:
                    res.append(chr(97+collum)+ str(row))
        row -= 1

    if row != 0:
        warning(f"row shold be 0. is {row}")

    return res




