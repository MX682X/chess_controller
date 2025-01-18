import logging
from time import sleep

import serial


class DISPLAY:
    def __init__(self, port):

        serial.Serial(port=port, baudrate=115200, timeout=.1).write(b"COM:reboot\n")

        sleep(0.01)
        self.conn = serial.Serial(port=port, baudrate=115200, timeout=.1)
        while True:
            if self.conn.in_waiting != 0:
                data = self.conn.readline()
                strdata = data.decode("utf-8").strip()
                if strdata == "Startup complete":
                    break
        self.scene = "0"

    def setscene(self, scene):
        if scene != self.scene:
            s = "COM:SC:" + scene + "\n"
            self.conn.write(s.encode("utf-8"))
            self.scene = scene
        else:
            print("Scene already set")

    # SCENE 1_0
    def Waitforgamemode(self):
        self.setscene("1_0")
        while True:
            if self.conn.in_waiting != 0:
                data = self.conn.readline()
                strdata = data.decode("utf-8").strip()
                if strdata.startswith("COM:BTN1_0:"):
                    match strdata:
                        case "COM:BTN1_0:CB":
                            return "black"
                        case "COM:BTN1_0:CW":
                            return "white"
                        case "COM:BTN1_0:CR":
                            return "Random"
                else:
                    logging.warning("Extpectet a Scene 1_0 Command")

    # SCENE 1_1

    def Addline(self, line: str):
        if self.scene == "1_1":
            linelist = line.split("\n")
            for l  in linelist:
                self.conn.write(("COM:1_1:push:" + l + "\n").encode("utf-8"))
        else:
            logging.warning("Addline can only be used in Scene 1_1")

    def Removeline(self,num = 1):
        if self.scene == "1_1":
            for _ in range(num):
                self.conn.write(b"COM:1_1:rm\n")
        else:
            logging.warning("Removeline can only be used in Scene 1_1")

    def Clearlines(self):
        if self.scene == "1_1":
            self.conn.write(b"COM:1_1:clr\n")
        else:
            logging.warning("Clearline can only be used in Scene 1_1")

    def Setlastline(self, line):
        self.Removeline()
        self.Addline(line)

    def button_Cmd_ready(self):
        return self.conn.in_waiting != 0 and self.scene == "1_1"

    def get_button_Cmc(self):
        if not self.button_Cmd_ready():
            return None

        data = self.conn.readline()
        strdata = data.decode("utf-8").strip()
        if strdata.startswith("COM:BTN1_1:"):
            match strdata:
                case "COM:BTN1_1:TB":
                    return "takeback"
                case "COM:BTN1_1:RES":
                    return "Resign"
                case "COM:BTN1_1:STB":
                    return "stable"
        else:
            logging.warning(f"Expected buttoncommand from scene 1_1. Got: {strdata}")

    def close(self):
        self.conn.write(b"COM:discon\n")
        self.conn.close()
