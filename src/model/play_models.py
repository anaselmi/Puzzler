from model.model import Model


class LogModel(Model):
    def __init__(self):
        super().__init__()
        self.logs = []

    def render(self, element):
        if self.rerender:
            element.clear()
            element.draw_logs(self.logs)
        self.rerender = False

    def handle(self, command, element, level):
        new_logs = level.send_logs()
        if not new_logs:
            return
        self.update_log(new_logs, element.max_logs)
        self.rerender = True

    def update(self, element, level):
        pass

    def update_log(self, new_logs, max_logs):
        self.logs += new_logs
        self._delete_extra_logs(max_logs)

    def clear_logs(self):
        self.logs = []

    def _delete_extra_logs(self, max_logs):
        while len(self.logs) >= max_logs:
            del self.logs[0]


class MapModel(Model):
    def __init__(self):
        super().__init__()
        self.tiles = []
        self.ents = []
        self.effects = []
