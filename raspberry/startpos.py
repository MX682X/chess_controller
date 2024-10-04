from toolbox import waitforstartpos
import serial

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

waitforstartpos(arduino)