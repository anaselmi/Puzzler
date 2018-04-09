import tcod
from consts import *


def handle_button(button, state):
    key = button.keychar

    if key == 'ESCAPE':
        return {"quit_game": True}

    if state is None:
        if key == "UP":
            return {"move": (0, -1)}
        elif key == "DOWN":
            return {"move": (0, 1)}
        elif key == "LEFT":
            return {"move": (-1, 0)}
        elif key == "RIGHT":
            return {"move": (1, 0)}
        elif key == "L":
            return {"state": "look"}

    elif state == "look":
        if key == "UP":
            return {"move_cursor": (0, -1)}
        elif key == "DOWN":
            return {"move_cursor": (0, 1)}
        elif key == "LEFT":
            return {"move_cursor": (-1, 0)}
        elif key == "RIGHT":
            return {"move_cursor": (1, 0)}
        elif key == "L":
            return {"state": None}
        elif key == "ENTER":
            return {"look", ...}

    return {}


class HandleButton:
    def __init__(self, state=None):
        self.state = state

    def process(self, button):
        key = button.keychar
        if key == 'ESCAPE':
            return "quit_game", True

        if self.state is None:
            if key == "UP":
                return "move", (0, -1)
            elif key == "DOWN":
                return "move", (0, 1)
            elif key == "LEFT":
                return "move", (-1, 0)
            elif key == "RIGHT":
                return "move", (1, 0)
            elif key == "l":
                self.state = "look"
                return "change_state", [None, "look"]

        elif self.state == "look":
            if key == "UP":
                return "move_cursor", (0, -1)
            elif key == "DOWN":
                return "move_cursor", (0, 1)
            elif key == "LEFT":
                return "move_cursor", (-1, 0)
            elif key == "RIGHT":
                return "move_cursor", (1, 0)
            elif key == "L":
                return "state", None
            elif key == "ENTER":
                return "look", ...
            elif key == "l":
                self.state = None
                return "change_state", ["look", None]

        return None, None

