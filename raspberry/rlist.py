import logging

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
            data = arduino.readline()
            strdata = data.decode("utf-8").strip()

            rlist.append(strdata)
            if len(rlist) >= 8:
                break
    return parseR(rlist)


arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

print(getreedlist(arduino))
