from enum import Enum
from pathlib import Path

from colortext import ColorText as Ct


class Mode(Enum):
    NORMAL = 0
    CALCULATE = 1
    FILE = 2
    LINK = 3

    def __str__(self):
        return self.name.lower()


class Environment:
    def __init__(self):
        self.path: Path = Path("./").resolve()
        self.mode = Mode.NORMAL

    def change_mode(self, mode: str) -> str:
        if mode == "normal":
            self.mode = Mode.NORMAL
            return Ct.YELLOW + "Changed to normal mode\n"
        elif mode == "calculate":
            self.mode = Mode.CALCULATE
            return Ct.YELLOW + "Changed to calculate mode\n"
        elif mode == "file":
            self.mode = Mode.FILE
            return Ct.YELLOW + "Changed to file mode\n"
        elif mode == "link":
            self.mode = Mode.LINK
            return Ct.YELLOW + "Changed to link mode\n"
        else:
            raise ValueError(f"Invalid mode \"{mode}\"")

    def get_mode(self):
        return self.mode

    def mode_color(self) -> str:
        if self.mode == Mode.NORMAL:
            return Ct.DEFAULT
        elif self.mode == Mode.CALCULATE:
            return Ct.BLUE
        elif self.mode == Mode.FILE:
            return Ct.GREEN
        elif self.mode == Mode.LINK:
            return Ct.CYAN
