import serial


class DISPLAY:
    def __init__(self, port):
        self.top = ""
        self.bottom = ""

        self.conn = serial.Serial(port=port, baudrate=9600, timeout=.1)

    def write(self):
        self.conn.write(b"clr\n")

        w = self.top + "\n" + self.bottom + "\n"
        self.conn.write(w.encode('utf-8'))


    # print("writing")

    def set_top(self, s):
        self.top = s

    def set_bottom(self, s):
        self.bottom = s

    def close(self):
        self.conn.write(b"clr\n")
        self.conn.write(b"Connection closed\n")
        self.conn.close()
