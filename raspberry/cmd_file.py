import queue
import threading
from dataclasses import dataclass


def cmd_fun(q:queue.Queue):
    print("CMD Ready")
    while True:
        cstr = input().strip()

        match cstr:
            case "stop":
                q.put(Stop())
                return
            case "stabilise":
                q.put(Stabilise())
            case "takeback":
                q.put(Takeback())
            case x:
                print(f"Unkonwn Command {x}")


class CMD_HANDLER:
    def __init__(self):
        self.q = queue.Queue()
        self.t = threading.Thread(target=cmd_fun,args=(self.q,),daemon=True)
        self.t.start()

    def get_cmd(self):
        if not self.q.empty():
            return self.q.get()

    def cmd_ready(self):
        return not self.q.empty()

    def cmd_close(self):
        self.t.join()


class BaseCommand:
    """A Class from wich all other Commandclasses inherit from."""
    pass

class Takeback(BaseCommand):
    """A Class Representing a Takeback Command.
    Should reset the Players last Move."""
    pass

class Stop(BaseCommand):
    """A Class Representing a Stop Command.
    Should Stop the Program immediately."""
    pass

class Stabilise(BaseCommand):
    """A Class Representing the Stabilise Command.
    Should Stabilise the Physical Board to the Virtual One."""

@dataclass
class Choice(BaseCommand):
    """A Class Representing the Choice Command.
    Represents the Players Choice about what game he wants to play.
    Args:
        Skill_Level(int): The Stockfish Skill Level the Player Chooses. Should be between 0 and 20.
        ColorChoice(str): The Color the Player chooses. Should be "CB"(Black),"CW"(White) or "CR" (Random)
    """
    ColorChoice:str
    Skill_Level:int


class Resign(BaseCommand):
    """A Class Representing the Resign Command.
    It means that the player Resigned. Currently not Implemented"""

class Restart(BaseCommand):
    """A Class Representing the Restart Command.
    Should restart the Game."""

