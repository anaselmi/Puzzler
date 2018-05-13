from src.state.state_abc import StateABC
from src.input_handling import update_action


class PlayState(StateABC):
    def __init__(self, ui, world):
        self.ui = ui
        self.world = world

    def enter(self):
        pass

    def exit(self):
        pass

    def render(self, console):
        self.ui.render(console)

    def update(self):
        pass

    def handle(self, action):
        pass
