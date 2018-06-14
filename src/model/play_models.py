from consts import *
from commands import update_command_dec
from model.model import Model


class LogModel(Model):
    name = LOG

    def __init__(self):
        name = LogModel.name
        super().__init__(name)
        self.logs = []

    def clear(self, element, level):
        pass

    @update_command_dec
    def handle(self, element, level, command=None):
        new_logs = level.send_logs()
        if not new_logs:
            return
        self.update_log(new_logs, element.height)
        self.rerender = True

    def update(self, element, level):
        if self.rerender:
            element.clear()
            element.draw_logs(self.logs)
        self.rerender = False

    def update_log(self, new_logs, max_logs):
        self.logs += new_logs
        self._delete_extra_logs(max_logs)

    def clear_logs(self):
        self.logs = []

    def _delete_extra_logs(self, max_logs):
        while len(self.logs) >= max_logs:
            del self.logs[0]


class TileModel(Model):
    name = TILE

    def __init__(self):
        name = TileModel.name
        super().__init__(name)
        self.tiles = []
        self.ents = []
        self.effects = []
