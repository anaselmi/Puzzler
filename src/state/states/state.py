class State:
    def __init__(self, stack):
        self.stack = stack

    def enter(self, screen):
        pass

    def exit(self):
        pass

    def start(self):
        pass

    def handle(self, command):
        pass

    def update(self, dx):
        pass

    def render(self, screen):
        pass
