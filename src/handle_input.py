import tcod
from consts import *

# TODO: Add integration
# TODO: Use handle_keys and dictionaries to parse and perform actions


def handle_keys(key):
    # Function that figures out what key was last pressed, performs said action
    key = key.vk
    if key == tcod.KEY_UP:
        return {"move": (0, -1)}
    elif key == tcod.KEY_DOWN:
        return {"move": (0, 1)}
    elif key == tcod.KEY_LEFT:
        return {"move": (-1, 0)}
    elif key == tcod.KEY_RIGHT:
        return {"move": (1, 0)}
    elif key == tcod.KEY_ESCAPE:
        return {"exit": True}
    elif key == tcod.KEY_0:
        return {"text_scroll": True}

    return {}


