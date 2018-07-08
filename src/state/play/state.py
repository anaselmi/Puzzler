import commands as com

from consts import *
from state.play.elements import TileElement, LogElement
from state.play.controllers import TileController, LogController
from state.state import State


class PlayState(State):
    def __init__(self, stack, level):
        super().__init__(stack, com.COMS_PLAY)
        self.level = level

    def enter(self, screen):
        self._create_elems(screen)
        self._create_ctrls()
        self.add_handler(self.level)

    def exit(self):
        pass

    def start(self):
        pass

    def update(self):
        for updater, command in self.coms:
            updater.update(command)

    def draw(self):
        [ctrl.draw() for ctrl in self.ctrls]

    def render(self, screen):
        [elem.render(screen) for elem in self.elems]

    def reset(self):
        super().reset()
        self.coms.append([self.level, {}])

    # TODO: Should use screen to determine size of elements.
    def _create_elems(self, screen):
        # TODO: Remove while loop. Only here so Pycharm thinks screen argument is being used
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

    def _create_ctrls(self):
        self.log_ctrl = LogController(self.log_elem)
        self.ctrls.append(self.log_ctrl)
        self.add_handler(self.log_ctrl, self.level)

        self.tile_ctrl = TileController(self.tile_elem)
        self.ctrls.append(self.tile_ctrl)
        self.add_handler(self.tile_ctrl, self.level)
