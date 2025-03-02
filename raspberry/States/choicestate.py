import logging
from random import choice

import chess

import States.basestate
from cmd_file import Choice

# Hack for IDE Support
if False:
    from statemachine import Machine


class Choicestate(States.basestate.State):
    """This State is active While the Player Chooses his Color and the Strength of the Engine"""
    def __init__(self, machine: "Machine"):
        self.machine = machine

    def activate(self):
        logging.info("Activating choicestate")

        self.machine.State = self
        self.machine.display.setscene("Choice")

    def command_handle(self,command):
        if isinstance(command,Choice):
            self.choice(command.ColorChoice,command.Skill_Level)
        else:
            logging.warning(f"Unknown Command: {command}")


    def choice(self,colur:str,strength:int):

        match colur:
            case "CB":
                self.machine.comcoluour = chess.WHITE
            case"CR":
                self.machine.comcoluour = choice([chess.BLACK,chess.WHITE])
            case "CW":
                self.machine.comcoluour = chess.BLACK
            case x:
                logging.warning(f"Unknown colour {x}. Choosing random Colour instead")
                self.machine.comcoluour = choice([chess.BLACK, chess.WHITE])

        self.machine.engine.configure({"Skill Level": strength})

        self.machine.skilllevel = strength

        self.machine.display.setscene("Game")
        self.machine.display.Addline("Waiting for Startposition")

        self.machine.stablestate.activate()

