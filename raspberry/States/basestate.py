# Hack for IDE Support
if False:
    from statemachine import Machine


class State:
    def __init__(self, machine: "Machine"):
        self.machine = machine

    def activate(self):
        raise NotImplementedError

    def place(self, pos):
        pass

    def take(self, pos):
        pass
    def stop(self):
        pass

    def takeback(self):
        pass

    def Stabilise(self):
        pass
