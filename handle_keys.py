import tcod
import sys
from consts import *


def get_key():
    key = tcod.console_wait_for_keypress(True)
    return key


def handle_keys():
    key = get_key()
    if key.vk == tcod.KEY_UP:
        return "MOVE UP"
    if key.vk == tcod.KEY_DOWN:
        return "MOVE DOWN"
    if key.vk == tcod.KEY_LEFT:
        return "MOVE LEFT"
    if key.vk == tcod.KEY_RIGHT:
        return "MOVE RIGHT"

