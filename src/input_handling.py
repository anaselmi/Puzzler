class InputHandler:
    # Turns user input into strings that different game elements can parse
    # Although these strings are written with player input in mind, they can
    # be parsed by any game element that requires user input
    @staticmethod
    def handle(_input):
        _type = _input.type
        if _type == "KEYDOWN":
            key = _input.keychar
            if key == 'ESCAPE':
                return {"EXIT": True}
            if key == 'ENTER':
                return {"RETURN": True}
            elif key == "UP" or key == "KP8":
                return {"MOVE": "NORTH"}
            elif key == "DOWN" or key == "KP2":
                return {"MOVE": "SOUTH"}
            elif key == "LEFT" or key == "KP4":
                return {"MOVE": "WEST"}
            elif key == "RIGHT" or key == "KP6":
                return {"MOVE": "EAST"}
            elif key == "KP7":
                return {"MOVE": "NORTHWEST"}
            elif key == "KP1":
                return {"MOVE": "SOUTHWEST"}
            elif key == "KP9":
                return {"MOVE": "NORTHEAST"}
            elif key == "KP3":
                return {"MOVE": "SOUTHEAST"}

            elif key == "l":
                return {"LOOK": True}
        return {}


def update_action(action, result):
    # State did not consume action
    if result == {} or result is None:
        return action
    # State consumed action
    if result == action:
        return {}
    # State generated new action
    else:
        return result

