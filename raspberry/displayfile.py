import logging
from logging import warning
from time import sleep

import serial


class DISPLAY:
    def __init__(self, port):

        serial.Serial(port=port, baudrate=115200, timeout=.1).write(b"reboot\n")

        sleep(0.01)
        self.conn = serial.Serial(port=port, baudrate=115200, timeout=.1)

        #TODO: denhier durch ne statemachine ersetzen
        while True:
            if self.conn.in_waiting != 0:
                data = self.conn.readline()
                strdata = data.decode("utf-8").strip()
                if strdata == "Startup complete":
                    break
        self.scene = "Discon"

    def setscene(self, scene):
        if scene != self.scene:
            s = "SC:" + scene + "\n"
            self.conn.write(s.encode("utf-8"))
            self.scene = scene
        else:
            print("Scene already set")

    # SCENE 1_0
    def Waitforgamemode(self):
        self.setscene("Choice")
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
        if self.scene == "Game":
            linelist = line.split("\n")
            for l  in linelist:
                self.conn.write(("Game:push:" + l + "\n").encode("utf-8"))
        else:
            logging.warning("Addline can only be used in Scene Game")

    def Removeline(self,num = 1):
        if self.scene == "Game":
            for _ in range(num):
                self.conn.write(b"Game:rm\n")
        else:
            logging.warning("Addline can only be used in Scene Game")

    def Clearlines(self):
        if self.scene == "Game":
            self.conn.write(b"Game:clr\n")
        else:
            logging.warning("Addline can only be used in Scene Game")

    def Setlastline(self, line):
        self.Removeline()
        self.Addline(line)

    def button_Cmd_ready(self):
        return self.conn.in_waiting != 0

    def get_button_Cmc(self):
        if not self.button_Cmd_ready():
            return None

        data = self.conn.readline()
        strdata = data.decode("utf-8").strip()

        if strdata.startswith("["):
            warning("Display:" + strdata)
            return


        if strdata.startswith("Game_BTN:"):
            match strdata:
                case "Game_BTN:TB":
                    return "takeback"
                case "Game_BTN:RES":
                    return "Resign"
                case "Game_BTN:STB":
                    return "stable"
        elif strdata.startswith("Choice_BTN:"):
            return strdata[-2:]
        else:
            logging.warning(f"Expected buttoncommand from scene Game. Got: {strdata}")

    def close(self):
        self.conn.write(b"COM:discon\n")
        self.conn.close()
