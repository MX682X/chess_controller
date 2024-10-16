from RPLCD.gpio import CharLCD
from RPi import GPIO


class DISPLAY:
    def __init__(self):
        self.top = ""
        self.bottom = ""
        self.lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode=GPIO.BOARD, cols=16, rows=2)

    def write(self):
        print("writing")
        self.lcd.clear()
        self.lcd.write_string(self.top)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(self.bottom)

    def set_top(self, s):
        self.top = s

    def set_bottom(self, s):
        self.bottom = s

    def close(self):
        self.lcd.close(True)
