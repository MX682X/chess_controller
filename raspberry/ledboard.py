import serial


class ledboard:
    def __init__(self,ser: serial.serialposix.Serial):
        self.con = ser

    def led_turnon(self, field: str):
        s = "s" + field + "\n"
        self.con.write(s.encode())

    def led_turnoff(self, field: str):
        s = "k" + field + "\n"
        self.con.write(s.encode())

    def clrall(self):
        for row in range(1, 9):
            for col in range(97, 97 + 8):
                self.led_turnoff( chr(col) + str(row))