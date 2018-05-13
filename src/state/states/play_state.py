from src.input_handling import update_action
from src.state.states.state_abc import StateABC


class PlayState(StateABC):
    def __init__(self, ui, world):
        self.ui = ui
        self.world = world

        self.world_updated = True

    def enter(self):
        self.ui.update(action={}, world=self.world)

    def exit(self):
        pass

    def render(self, console):
        self.ui.render(console)

    def clear(self):
        self.ui.clear()

    def update(self, action):
        result = self.ui.update(action=action, world=self.world)
        action = update_action(action, result)
        paused = action.get("PAUSED")
        print(paused)
        if not paused:
            self.world.handle(action)
