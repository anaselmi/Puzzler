from src.input_handling import update_command
from src.state.states.state_abc import StateABC
from src.model.log_model import LogModel


class PlayState(StateABC):
    def __init__(self, ui, level):
        self.ui = ui
        self.level = level
        self.models = self._create_models(ui)

    def enter(self):
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
        log_elem = ui.log_element
        log_model = LogModel(log_elem)
        models.append(log_model)

        return models
