import logging

import serial

from toolbox import clrall, getreedlist, led_turnon, led_turnoff


def waitforpos(ser: serial.serialposix.Serial, pos: list[str]):
    clrall(ser)
    zuviel = []

    fehlt = pos

    istpos = getreedlist(ser)

    for i in istpos:
        if i in fehlt:
            fehlt.remove(i)

        else:
            zuviel.append(i)
            led_turnon(ser, i)

    for i in fehlt:
        led_turnon(ser, i)

    # print(f"fehlt: {fehlt}")
    # print(f"zuviel: {zuviel}")

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


def waitforstartpos(ser: serial.serialposix.Serial):
    startpos = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
             "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
             "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
             "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", ]
    waitforpos(ser,startpos)


if __name__ == "__main__":
    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)
    waitforstartpos(arduino)
