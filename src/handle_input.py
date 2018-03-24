import tcod
from consts import *

# TODO: Add integration
# TODO: Use handle_input and dictionaries to parse and perform actions


def handle_input(input):
    # Function that figures out what key was last pressed, performs said action
    key = input.key
    print(key)
    if key == "UP":
        return {"move": (0, -1)}
    elif key == "DOWN":
        return {"move": (0, 1)}
    elif key == "LEFT":
        return {"move": (-1, 0)}
    elif key == "RIGHT":
        return {"move": (1, 0)}
    elif key == 'ESCAPE':
        return {"exit": True}
    # TODO
    elif key == tcod.KEY_0:
        return {"message_scroll": True}

    return {}


