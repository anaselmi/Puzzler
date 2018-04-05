from ecs_manager import *


class Renderable(Component):

    def __init__(self, tags):
        valid_actions = ["draw", "clear"]
        super().__init__(self, valid_actions, tags)

    def parse(self, event):
        pass

