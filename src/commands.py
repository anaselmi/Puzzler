from consts import *


def _handle_movement(key):
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


def handle(_input):
    _type = _input.type
    if _type == "KEYDOWN":
        key = _input.keychar
        move = _handle_movement(key)
        if move:
            return move
        if key == 'ENTER':
            return C_ENTER
        elif key == 'ESCAPE':
            return C_EXIT
        elif key == "l":
            return {"look": True}
    return {}


def update_command(command, result):
    # State did not consume action
    if result == {} or result is None:
        return command
    # State consumed action
    if result.get("consumed"):
        return {}
    # State generated new action
    else:
        return result

