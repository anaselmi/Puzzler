from commands import update_command
from state.states.state import State
from model.play_models import LogModel
from model.play_models import TileModel
from ui.elements.play_elements import TileElement
from ui.elements.play_elements import LogElement


class PlayState(State):
    def __init__(self, stack, level):
        super().__init__(stack)
        self.level = level

    def enter(self, screen):
        self._create_elements(screen)
        self._create_models()

    def exit(self):
        pass

    def start(self):
        pass

    def render(self, screen):
        self.tile_mod.render(self.tile_elem, screen)
        self.log_mod.render(self.log_elem, screen)

    def handle(self, command):
        result = self.log_mod.handle(command=command, level=self.level, element=self.log_elem)
        command = update_command(command, result)
        self.level.handle(command)

    def update(self, dx):
        pass

    def _create_elements(self, screen):
        sc_size = screen.width, screen.height
        self.tile_elem = TileElement(pos=(0, 0), sc_size=sc_size)
        self.log_elem = LogElement(pos=(0, self.tile_elem.c_height), sc_size=sc_size)

    def _create_models(self):
        self.tile_mod = TileModel()
        self.log_mod = LogModel()
