class InputHandler:
    @staticmethod
    def handle(_input):
        _type = _input.type
        if _type == "KEYDOWN":
            key = _input.keychar
            if key == 'ESCAPE':
                return {"exit": True}
            if key == 'ENTER':
                return {"return": True}
            elif key == "UP" or key == "KP8":
                return {"move": "north"}
            elif key == "DOWN" or key == "KP2":
                return {"move": "south"}
            elif key == "LEFT" or key == "KP4":
                return {"move": "west"}
            elif key == "RIGHT" or key == "KP6":
                return {"move": "east"}
            elif key == "KP7":
                return {"move": "northwest"}
            elif key == "KP1":
                return {"move": "southwest"}
            elif key == "KP9":
                return {"move": "northeast"}
            elif key == "KP3":
                return {"move": "southeast"}

            elif key == "l":
                return {"look": True}
        return {}


def update_command(command, result):
    # State did not consume action
    if result == {} or result is None:
        return command
    # State consumed action
    if result == command:
        return {}
    # State generated new action
    else:
        return result

