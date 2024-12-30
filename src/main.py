from colortext import ColorText as Ct
from config import Config
from environment import Environment, Mode
from file import file_eval
from link import link_eval
from shortcut import shortcut_eval


def print_info(config: Config):
    print(f"{Ct.BLUE}{config['name']} {Ct.GREEN}v{config['version']}")
    print(Ct.CYAN + f"made by {config['author']}\n" + Ct.DEFAULT)


def eval_input(user_input: str, config: Config, env: Environment) -> str:
    args = user_input.split(" ")
    if args[0] == "exit":
        raise KeyboardInterrupt
    elif args[0][0] == "@":  # shortcut
        is_command, result = shortcut_eval(user_input[1:], config, env)
        if is_command:
            commands: list[str] = result.split(";")
            result = ""
            for command in commands:
                result += eval_input(command.strip(), config, env)
            return result
        else:
            return result
    elif args[0] == "mode":
        return env.change_mode(args[1])
    elif env.get_mode() == Mode.NORMAL:
        pass
    elif env.get_mode() == Mode.CALCULATE:
        return Ct.BLUE + str(eval(user_input))
    elif env.get_mode() == Mode.FILE:
        return file_eval(args, config, env)
    elif env.get_mode() == Mode.LINK:
        return link_eval(args, config, env)
    return user_input


def read_eval_print_loop(config: Config, env: Environment):
    while True:
        try:
            print(env.mode_color() + f"{config['name']}({env.get_mode()} mode)")
            print(f"{Ct.GREY}{env.path}{Ct.DEFAULT}")
            user_input = input(">>> ")
            print(eval_input(user_input, config, env) + Ct.DEFAULT)
        except KeyboardInterrupt:
            print(Ct.YELLOW + "KeyboardInterrupt\n" + Ct.DEFAULT)
            break
        except ValueError as e:
            print(Ct.RED + f"ValueError: {e}\n" + Ct.DEFAULT)


def main():
    config = Config()
    env = Environment()
    print_info(config)
    read_eval_print_loop(config, env)


if __name__ == "__main__":
    main()
