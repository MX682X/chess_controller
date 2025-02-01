import logging

import States.basestate

# Hack for IDE Support
if False:
    from statemachine import Machine


class stablestate(States.basestate.State):
    def __init__(self, machine: "Machine"):
        self.istpos = None
        self.fehlt = None
        self.zuviel = None
        self.machine = machine

    def activate(self, extraturnon=None):
        logging.info("Activating Stablestate")
        self.machine.State = self



        self.machine.leds.clrall()
        self.zuviel = []
        self.fehlt = self.machine.boardstrlist
        self.istpos = self.machine.poslist

        for i in self.istpos:
            if i in self.fehlt:
                self.fehlt.remove(i)

            else:
                self.zuviel.append(i)
                self.machine.leds.led_turnon(i)

        for i in self.fehlt:
            self.machine.leds.led_turnon(i)

        # print(f"fehlt: {fehlt}")
        # print(f"zuviel: {zuviel}")

        if extraturnon is not None:
            self.machine.leds.led_turnon(extraturnon)

        if self.fehlt == [] and self.zuviel == []:
            self.machine.movestate.activate()
            return

        print(self.machine.board)

    def place(self, field):

        if field in self.fehlt:
            self.fehlt.remove(field)
            self.machine.leds.led_turnoff(field)
        else:
            self.zuviel.append(field)
            self.machine.leds.led_turnon(field)

        if self.fehlt == [] and self.zuviel == []:
            self.machine.movestate.activate()
            return

    def take(self, field):
        if field in self.zuviel:
            self.zuviel.remove(field)
            self.machine.leds.led_turnoff(field)

        else:
            self.fehlt.append(field)
            self.machine.leds.led_turnon(field)

        if self.fehlt == [] and self.zuviel == []:
            self.machine.movestate.activate()


    def takeback(self):
        self.machine.board.pop()
        self.machine.board.pop()
        self.activate()

    def Stabilise(self):
        logging.info("Already Stabilising")
