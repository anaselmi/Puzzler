from consts import *
from commands import update_result
from controller.controller import Controller
from logic.level import Level


class LogController(Controller):
    name = LOG

    def __init__(self, element):
        name = LogController.name
        super().__init__(name, element)
        self.logs = []

    def clear(self, element, data: Level):
        pass

    @update_result
    def handle(self, data: Level, command=None):
        pass

    def update(self, data: Level, command=None):
        new_logs = data.send_logs()
        if not new_logs:
            return
        self.add_logs(new_logs, self.element.max_logs)
        self.redraw = True

    def draw(self):
        if self.redraw:
            self.element.clear()
            self.element.draw_logs(self.logs)
        self.redraw = False

    def add_logs(self, new_logs, max_logs):
        self.logs += new_logs
        self._delete_extra_logs(max_logs)

    def clear_logs(self):
        self.logs = []

    def _delete_extra_logs(self, max_logs):
        while len(self.logs) >= max_logs:
            del self.logs[0]


class TileController(Controller):
    name = TILE

    def __init__(self, element):
        name = TileController.name
        super().__init__(name, element)
        self.tiles = []
        self.ents = []
        self.effects = []

    @update_result
    def handle(self, data: Level, command=None):
        pass

    def update(self, data: Level, command=None):
        pass

    def draw(self):
        pass
