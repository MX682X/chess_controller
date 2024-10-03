import logging


class MOVEHANDLER:
    def __init__(self):
        self.Firsttaken = ""
        self.Secondtaken = ""

    def addtake(self, field: str):
        if self.Secondtaken != "":
            logging.warning(f"Taken three pieces! forgetting about {self.Secondtaken}.")

        self.Secondtaken = self.Firsttaken

        self.Firsttaken = field

    def clear(self):
        self.Firsttaken = ""
        self.Secondtaken = ""

    def addplace(self, field):

        if self.Firsttaken == "" and self.Secondtaken == "":
            logging.warning(f"Placing two pieces in a Row! ignoring placing {field}")
            return None

        if self.Firsttaken != "" and self.Secondtaken == "":
            sMove = self.Firsttaken + field
            self.clear()
            if sMove[:2] == sMove[2:]:
                sMove = "0000"
            return sMove

        if field == self.Firsttaken:
            sMove = self.Secondtaken + field
            self.clear()
            return sMove

        if field == self.Secondtaken:
            sMove = self.Firsttaken + field
            self.clear()
            return sMove

        if field != self.Firsttaken and field != self.Secondtaken:
            logging.warning(f"Invalid first Take. Igioring {self.Firsttaken}.")

            sMove = self.Secondtaken + field

            self.clear()

            if sMove[:2] == sMove[2:]:
                sMove = "0000"
            return sMove

        logging.warning("How did we get here?")
        return None
