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
            data = ser.readline()
            strdata = data.decode("utf-8").strip()

            rlist.append(strdata)
            if len(rlist) >= 8:
                break
    return parseR(rlist)


def waitforstartpos(ser: serial.serialposix.Serial):
    zuviel = []

    startpos = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
                "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
                "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
                "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", ]

    istpos = getreedlist(ser)

    for i in istpos:
        if i in startpos:
            startpos.remove(i)
        else:
            zuviel.append(i)

    while True:
        if ser.in_waiting != 0:
            data = ser.readline()
            strdata = data.decode("utf-8").strip()
            # print(strdata)
            match strdata[0]:
                case "t":
                    pas
                case "p":
                    pass
                case _:
                    logging.warning("unkown Beginning: " + strdata[0])
