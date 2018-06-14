from consts import *
from commands import update_command_dec
from model.play_models import LogModel
from model.play_models import TileModel
from state.state import State
from ui.elements.play_elements import LogElement
from ui.elements.play_elements import TileElement


class PlayState(State):
    def __init__(self, stack, level):
        super().__init__(stack)
        self.level = level
        self.elems = []
        self.mods = []
        self.pairs = []

    def enter(self, screen):
        self._create_elems(screen)
        self._create_mods()

    def exit(self):
        pass

    def start(self):
        pass

    def dispatch(self, command):
        for mod, elem in self.pairs:
            command = mod.handle(command=command, level=self.level, element=elem)
        command = self.level.handle(command=command)
        return command

    def update(self):
        pass

    def render(self, screen):
        [elem.render(screen) for elem in self.elems]

    def reset(self):
        [elem.reset() for elem in self.elems]

    # TODO: Should use screen to determine size of elements.
    def _create_elems(self, screen):
        # TODO: Remove while loop.
        # Loop is only here so Pycharm thinks screen is being used.
        while False:
            print()
            print(screen)
            print()
        tile_pos = (0, 0)
        tile_size = TILE_SIZE
        self.tile_elem = TileElement(pos=tile_pos, size=tile_size)
        self.elems.append(self.tile_elem)
        log_pos = (0, self.tile_elem.con.height)
        log_size = LOG_SIZE
        self.log_elem = LogElement(pos=log_pos, size=log_size)
        self.elems.append(self.log_elem)

    def _create_mods(self):
        self.log_mod = LogModel()
        self.mods.append(self.log_mod)
        log_pair = self.log_mod, self.log_elem
        self.pairs.append(log_pair)

        self.tile_mod = TileModel()
        self.mods.append(self.log_mod)
        tile_pair = self.tile_mod, self.tile_elem
        self.pairs.append(tile_pair)
