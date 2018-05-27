from src.model.model_abc import ModelABC


class LogModel(ModelABC):
    def __init__(self, element):
        super().__init__()
        self.logs = []

        self.elem = element
        self.max_logs = self.elem.height - 1

    def render(self):
        if self.rerender:
            self.elem.clear()
            self.elem.draw_log(self.logs)
        self.rerender = False

    def handle(self, command, level):
        pass

    def update(self, level):
        new_logs = level.send_logs()
        if not new_logs:
            return
        self.update_log(new_logs)
        self.rerender = True

    def update_log(self, logs):
        self.logs += logs
        self._delete_old_logs()

    def _delete_old_logs(self):
        while len(self.logs) >= self.max_logs:
            del self.logs[0]
