import argparse
import os
from pathlib import Path

from colortext import ColorText as Ct
from config import Config
from environment import Environment


def file_eval(args: list[str], config: Config, env: Environment) -> str:
    ls_parser = argparse.ArgumentParser(prog="ls", description="List files and directories")
    ls_parser.add_argument("path", nargs="?", default="./")
    ls_parser.add_argument("-r", "--recursive", action="store_true", help="List recursively")

    if args[0] == "ls":
        args = ls_parser.parse_args(args[1:])
        return ls(args.path, env, args.recursive, 0)
    elif args[0] == "cd":
        if len(args) < 2:
            raise ValueError("No path provided")
        return cd(str_to_path(args[1], env), env)
    elif args[0] == "op":  # open file
        if len(args) < 2:
            raise ValueError("No file provided")
        return open_file(str_to_path(args[1], env))
    else:
        return Ct.RED + f"Invalid command \"{args[0]}\""


def ls(directory: Path, env: Environment, recursive: bool, tab: int) -> str:
    result = ''
    directory = env.path / directory
    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")
    for dire in directory.iterdir():
        if dire.is_dir():
            result += (Ct.CYAN +
                       '|   ' * (tab - 1) +
                       '└---' * (1 if tab > 0 else 0) +
                       f"{dire.name}\n")
            if recursive:
                result += ls(dire, env, recursive, tab + 1)
    for file in directory.iterdir():
        if file.is_file():
            result += (Ct.CYAN + '|   ' * (tab - 1) +
                       '└---' * (1 if tab > 0 else 0) +
                       Ct.GREEN + f"{file.name}\n")
    return result


def cd(path: Path, env: Environment) -> str:
    if path.is_dir():
        env.path = path
        return Ct.YELLOW + f"Changed directory to {env.path}\n"
    else:
        raise ValueError(f"Not a directory: {path}")


def open_file(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")
    os.startfile(path)
    return Ct.YELLOW + f"{path.name} opened\n"


def str_to_path(string: str, env: Environment) -> Path:
    if Path(string).is_absolute():
        return Path(string)
    else:
        return (env.path / string).resolve()