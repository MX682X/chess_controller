from logging import warning

import serial

import rlist


def clrall(ser: serial.serialposix.Serial):
    for row in range(1, 9):
        for col in range(97, 97 + 8):
            s = "k" + chr(col) + str(row) + "\n"
            ser.write(s.encode())


arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

clrall(arduino)

rlist = rlist.getreedlist(arduino)

for i in rlist:
    s = "s" + i + "\n"
    arduino.write(s.encode())

while True:
    if arduino.in_waiting != 0:
        data = arduino.readline()
        strdata = data.decode("utf-8").strip()
        # print(strdata)
        if strdata[0] == "t":
            s = "k" + strdata[1:3] + "\n"
            arduino.write(s.encode())

        elif strdata[0] == "p":
            s = "s" + strdata[1:3] + "\n"
            arduino.write(s.encode())


        else:
            warning("unkown Beginning: " + strdata[0])
