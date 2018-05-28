from input_handling import update_command
from state.states.state import State
from model.log_model import LogModel


class PlayState(State):
    def __init__(self, stack, ui, level):
        super().__init__(stack)
        self.ui = ui
        self.level = level
        self.models = self._create_models(ui)

    def enter(self, level):
        self.level = level
        self.ui.handle(command={}, level=self.level)

    def exit(self):
        pass

    def render(self, console):
        for model in self.models:
            model.render()
        self.ui.render(console)

    def handle(self, command):
        result = self.ui.handle(command=command, level=self.level)
        command = update_command(command, result)
        paused = command.get("paused")
        if not paused:
            self.level.handle(command)

    def update(self):
        for model in self.models:
            model.update(self.level)

    def _create_models(self, ui):
        models = []

        return models
