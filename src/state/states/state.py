class State:
    def __init__(self, stack, screen_size):
        self.stack = stack
        self.active = False

    def enter(self, level):
        pass

    def exit(self):
        pass

    def render(self, console):
        pass

    def update(self):
        pass

    def handle(self, command):
        pass
