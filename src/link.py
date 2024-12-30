import argparse
import json
from pathlib import Path

from colortext import ColorText as Ct
from config import Config
from environment import Environment
from file import cd, open_file


class LinkData:
    def __init__(self, config: Config):
        self.data_path = Path(config['datapath']).resolve()
        link_path = self.data_path / 'link.json'
        bat_path = self.data_path / 'bat.json'

        try:
            with open(link_path, 'r', encoding='utf-8') as f:
                self.links = json.load(f)
        except FileNotFoundError:
            self.links = {}
            with open(link_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(self.links, indent=4)
                f.write(json_str)

        try:
            with open(bat_path, 'r', encoding='utf-8') as f:
                self.bats = json.load(f)
        except FileNotFoundError:
            self.bats = {}
            with open(bat_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(self.bats, indent=4)
                f.write(json_str)

    def get_links(self) -> str:
        result = Ct.GREEN
        for name, path in self.links.items():
            result += f"{name}: \"{path}\"\n"
        return result

    def get_bats(self) -> str:
        result = Ct.BLUE
        for name, path in self.bats.items():
            result += f"{name}: \"{path}\"\n"
        return result

    def save_data(self) -> str:
        link_path = self.data_path / 'link.json'
        bat_path = self.data_path / 'bat.json'

        with open(link_path, 'w', encoding='utf-8') as f:
            json_str = json.dumps(self.links, indent=4)
            f.write(json_str)

        with open(bat_path, 'w', encoding='utf-8') as f:
            json_str = json.dumps(self.bats, indent=4)
            f.write(json_str)

        return Ct.YELLOW + "Data saved\n"

    def add_link(self, env: Environment, name: str, path: Path) -> str:
        if not Path(path).is_absolute():
            path = env.path / path
        if not path.is_file() and not path.is_dir():
            raise ValueError(f"Not a file or directory: {path}")
        self.links[name] = str(path)
        self.save_data()
        return Ct.YELLOW + f"Added link ({name}: \"{path}\")\n"

    def add_bat(self, env: Environment, name: str, path: Path) -> str:
        if not Path(path).is_absolute():
            path = env.path / path
        if not path.is_file() or path.suffix != ".bat":
            raise ValueError(f"Not a bat: {path}")
        self.bats[name] = str(path)
        self.save_data()
        return Ct.YELLOW + f"Added bat ({name}: \"{path}\")\n"

    def click_link(self, env: Environment, name: str) -> str:
        if name not in self.links:
            raise ValueError(f"Link \"{name}\" not found")
        path = Path(self.links[name])
        if path.is_dir():
            return cd(path, env)
        else:
            return open_file(path)

    def run_bat(self, name: str) -> str:
        if name not in self.bats:
            raise ValueError(f"Bat \"{name}\" not found")
        path = Path(self.bats[name])
        open_file(path)
        return Ct.YELLOW + f"Ran bat ({name}: \"{path}\")\n"


link_data = None


def link_eval(args: list[str], config: Config, env: Environment) -> str:
    add_parser = argparse.ArgumentParser(prog="add", description="Add link or bat")
    add_parser.add_argument("-b", "--bat", action="store_true", help="Add bat")
    add_parser.add_argument("name", type=str, help="Name of link or bat")
    add_parser.add_argument("path", type=str, help="Path of link or bat")

    global link_data
    if link_data is None:
        data = LinkData(config)
    else:
        data = link_data

    if args[0] == "links":
        return data.get_links()
    elif args[0] == "bats":
        return data.get_bats()
    elif args[0] == "save":
        return data.save_data()
    elif args[0] == "add":
        args = add_parser.parse_args(args[1:])
        if args.bat:
            return data.add_bat(env, args.name, Path(args.path))
        else:
            return data.add_link(env, args.name, Path(args.path))
    elif args[0] == "link":
        return data.click_link(env, args[1])
    elif args[0] == "bat":
        return data.run_bat(args[1])
    else:
        return Ct.RED + f"Invalid command \"{args[0]}\""
