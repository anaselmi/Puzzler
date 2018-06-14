from commands import update_command


class Model:
    def __init__(self, name):
        self.name = name
        self.rerender = True

    def handle(self, element, data, command=None):
        pass

    def update(self, element, data):
        pass
