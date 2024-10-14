from logging import warning
from time import sleep

import serial

import toolbox

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

toolbox.clrall(arduino)

rlist = toolbox.getreedlist(arduino)

for i in rlist:
    toolbox.led_turnon(arduino, i)

while True:
    sleep(0.1)
    if arduino.in_waiting != 0:
        data = arduino.readline()
        strdata = data.decode("utf-8").strip()
        # print(strdata)
        if strdata[0] == "t":
            toolbox.led_turnoff(arduino, strdata[1:3])

        elif strdata[0] == "p":
            toolbox.led_turnon(arduino, strdata[1:3])


        else:
            warning("unkown Beginning: " + strdata[0])
