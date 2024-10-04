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

    ser.readline()
    return parseR(rlist)


def led_turnon(ser: serial.serialposix.Serial, field: str):
    s = "s" + field + "\n"
    ser.write(s.encode())


def led_turnoff(ser: serial.serialposix.Serial, field: str):
    s = "k" + field + "\n"
    ser.write(s.encode())


def waitforstartpos(ser: serial.serialposix.Serial):
    zuviel = []

    fehlt = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
             "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
             "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
             "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", ]

    istpos = getreedlist(ser)

    for i in istpos:
        if i in fehlt:
            fehlt.remove(i)

        else:
            zuviel.append(i)
            led_turnon(ser,i)

    for i in fehlt:
        led_turnon(ser,i)

    while True:
        if ser.in_waiting != 0:
            data = ser.readline()
            strdata = data.decode("utf-8").strip()
            # print(strdata)
            match strdata[0]:
                case "t":
                    field = strdata[1:3]
                    if field in zuviel:
                        zuviel.remove(field)
                        led_turnoff(ser, field)

                    else:
                        fehlt.append(field)
                        led_turnon(ser, field)

                    if fehlt == [] and zuviel == []:
                        return
                case "p":
                    field = strdata[1:3]
                    if field in fehlt:
                        fehlt.remove(field)
                        led_turnoff(ser, field)
                    else:
                        zuviel.append(field)
                        led_turnon(ser, field)
                    if fehlt == [] and zuviel == []:
                        return
                case _:
                    logging.warning("unknown Beginning: " + strdata[0])


def clrall(ser: serial.serialposix.Serial):
    for row in range(1, 9):
        for col in range(97, 97 + 8):
            led_turnoff(ser, chr(col) + str(row))
