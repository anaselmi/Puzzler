from src.input_handling import update_command
from src.state.states.state_abc import StateABC


class PlayState(StateABC):
    def __init__(self, ui, level):
        self.ui = ui
        self.level = level

        self.world_updated = True

    def enter(self):
        self.ui.handle(command={}, level=self.level)

    def exit(self):
        pass

    def render(self, console):
        self.ui.render(console)

    def clear(self):
        self.ui.clear()

    def handle(self, command):
        result = self.ui.handle(command=command, level=self.level)
        command = update_command(command, result)
        paused = command.get("paused")
        if not paused:
            self.level.handle(command)

    def update(self):
        pass
