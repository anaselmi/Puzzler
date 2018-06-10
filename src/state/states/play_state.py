from commands import update_command
from state.states.state import State
from model.play_models import LogModel
from model.play_models import MapModel
from ui.elements.element import MapElement
from ui.elements.element import LogElement


class PlayState(State):
    def __init__(self, stack, level):
        super().__init__(stack)
        self.level = level

    def enter(self, screen):
        self._create_models(screen)

    def exit(self):
        pass

    def render(self, console):
        self.map_model

    def handle(self, command):
        result = self.log_model.handle(command=command, level=self.level)
        command = update_command(command, result)
        paused = command.get("paused")
        if not paused:
            self.level.handle(command)

    def update(self, dx):
        pass

    def _create_elements(self, screen):
        sc_size = screen.width, screen.height
        self.map_elem = MapElement(pos=(0, 0), sc_size=sc_size)
        self.log_elem = LogElement(pos=(0, self.map_elem.c_height), sc_size=sc_size)

    def _create_models(self):
        self.map_elem = MapModel()
        self.log_mod = LogModel()
