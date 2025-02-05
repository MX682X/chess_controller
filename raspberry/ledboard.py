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
        self.con.write(b"o\n")