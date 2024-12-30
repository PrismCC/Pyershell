import json
from pathlib import Path

from colortext import ColorText as Ct
from config import Config
from environment import Environment


class Shortcuts:
    def __init__(self, config: Config):
        self.shortcut_path = Path(config['shortcut_path']).resolve()

        try:
            with open(self.shortcut_path, 'r', encoding='utf-8') as f:
                self.shortcuts = json.load(f)
        except FileNotFoundError:
            self.shortcuts = {
                "mn": "mode normal",
                "mc": "mode calculate",
                "mf": "mode file",
                "ml": "mode link",
            }
            with open(self.shortcut_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(self.shortcuts, indent=4)
                f.write(json_str)

    def add_shortcut(self, name: str, command: str) -> str:
        self.shortcuts[name] = command
        self.save_shortcuts()
        return Ct.YELLOW + f"Added shortcut \"{name}\"\n"

    def remove_shortcut(self, name: str):
        del self.shortcuts[name]
        self.save_shortcuts()
        return Ct.YELLOW + f"Removed shortcut \"{name}\"\n"

    def get_shortcuts(self) -> str:
        result = ""
        for name, commands in self.shortcuts.items():
            result += Ct.BLUE + f"{name}:\n"
            for command in commands.split(";"):
                result += Ct.CYAN + f"\t{command.strip()}\n"
        return result

    def save_shortcuts(self) -> str:
        with open(self.shortcut_path, 'w', encoding='utf-8') as f:
            json_str = json.dumps(self.shortcuts, indent=4)
            f.write(json_str)
        return Ct.YELLOW + "Shortcuts saved\n"

    def use_shortcut(self, name: str) -> str:
        if name not in self.shortcuts:
            raise ValueError(f"Shortcut \"{name}\" not found")
        return self.shortcuts[name]


shortcuts = None


def shortcut_eval(string: str, config: Config, env: Environment) -> (bool, str):
    global shortcuts
    if shortcuts is None:
        shortcuts = Shortcuts(config)

    args = string.split(" ")
    if args[0] == "+":
        if len(args) < 3:
            raise ValueError("Shortcut name and command required")
        return False, shortcuts.add_shortcut(args[1], ' '.join(args[2:]))
    elif args[0] == "-":
        if len(args) < 2:
            raise ValueError("Shortcut name required")
        return False, shortcuts.remove_shortcut(args[1])
    elif args[0] == "list":
        return False, shortcuts.get_shortcuts()
    elif args[0] == "save":
        return False, shortcuts.save_shortcuts()
    else:
        return True, shortcuts.use_shortcut(args[0])
