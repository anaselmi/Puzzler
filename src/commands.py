from tdl.event import Event, KeyDown
from consts import *
from typing import Union


def _parse_keydown_movement(key: str) -> dict:
    move = C_MOVE
    direction = None

    if key == "UP" or key == "KP8":
        direction = "north"
    elif key == "DOWN" or key == "KP2":
        direction = "south"
    elif key == "LEFT" or key == "KP4":
        direction = "south""west"
    elif key == "RIGHT" or key == "KP6":
        direction = "east"
    elif key == "KP7":
        direction = "northwest"
    elif key == "KP1":
        direction = "southwest"
    elif key == "KP9":
        direction = "northeast"
    elif key == "KP3":
        direction = "southeast"
    if direction is None:
        return {}

    move[C_K_MOVE] = direction
    return move


def parse_keydown(_input: KeyDown) -> dict:
    """

        :param KeyDown _input: Event signifying a keyboard button has been pressed.
        :return dict: The command that _input is mapped to.
        """
    key = _input.keychar
    move = _parse_keydown_movement(key)
    if move:
        return move
    if key == 'ENTER':
        return C_ENTER
    elif key == 'ESCAPE':
        return C_EXIT
    elif key == "l":
        return C_LOOK

    return {}


def parse_input(_input: Event) -> dict:
    """Generates a command based on _input.

    Notes:
        Multiple _input arguments can return the same command. Ex: Both UP and KP8 return {move: north}.
        Functions/methods that pass commands around must be called dispatch, while those that
        parse commands and modify gamestate must be called handle.

    :param Event _input: Represents player input from the keyboard or mouse.
    :return dict: Command the _input is mapped to.
    """
    if isinstance(_input, KeyDown):
        return parse_keydown(_input)

    return {}


def update_command(command: dict, result: Union[dict, None]) -> dict:
    """Generates a new command based on command, and the result of feeding command to a function/method.

    Notes:
        Result may be none because functions/methods implicitly return None.
        An empty command is simply an empty dictionary.

    :param dict command: The original command argument received by the function.
    :param Union[dict, None] result: The value returned by the function.
    :return dict: The new command determined by command and result.
                  If result is None or an empty command, command will be returned.
                  If result is a consumed command, an empty command will be returned.
                  If result is any other command, result is returned.
    """
    # Command has been ignored.
    if result == {} or result is None:
        return command
    # Command has been consumed.
    if result.get(C_K_CONSUMED):
        return {}
    # A new command has been generated.
    else:
        return result


def update_command_dec(func):
    """Changes the return value of functions/methods that handle and return commands.

    :param func: Function/Method to be wrapped. Must have a keyword argument called command.
    Must return Union[dict, None]. Must be named handle or _handle.
    :return: Wrapper adding update command functionality to func. Wrapper returns dict.
    """
    valid_names = ["handle", "_handle"]
    name = func.__name__
    if name not in valid_names:
        raise ValueError(f"{name} is not a valid name")
    if not callable(func):
        raise TypeError("func must be callable")

    def wrapper(*args, **kwargs):
        # Command is a kwarg because methods and functions have differently ordered args.
        command = kwargs.get("command")
        if command is None:
            raise ValueError("Could not find command kwarg")
        result = func(*args, **kwargs)
        if result is not None and not isinstance(result, dict):
            raise TypeError("func did not return a dictionary or None")
        return update_command(command=command, result=result)
    return wrapper
