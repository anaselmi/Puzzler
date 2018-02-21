import tcod
import sys
from consts import *


def handle_keys():
    # Function that figures out what key was last pressed, returns string for action to perform
    key = tcod.console_wait_for_keypress(True)
    if key.vk == tcod.KEY_UP:
        return "MOVE UP"
    if key.vk == tcod.KEY_DOWN:
        return "MOVE DOWN"
    if key.vk == tcod.KEY_LEFT:
        return "MOVE LEFT"
    if key.vk == tcod.KEY_RIGHT:
        return "MOVE RIGHT"

