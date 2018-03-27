import tdl
from ecs_meta import Component
from src.consts import *

render_allowed_events = ["draw", "clear", "scroll"]


class RenderComponent(Component):

    def __init__(self, **kwargs):
        priority = 0
        super().__init__(priority, **kwargs)

    def parse(self, event):
        if not self.active:
            return None

        if event.type == "draw":
            self.tag_ensure(x=None, y=None, char="@", fg=WHITE, bg=BLACK)
            self.owner.manager.window.draw_char(self.x, self.y, self.char, self.x, self.y, self.char, bg=(0, 0, 0), fg=(255, 255, 255))

        elif event.type == "clear":
            pass

        elif event.type == "scroll":
            pass

        else:
            pass

move_allowed_events = ["move"]


# TODO
class MoveComponent(Component):

    def __init__(self, **kwargs):
        priority = 1
        super().__init__(priority, **kwargs)

    def parse(self, event):
        if not self.active:
            return None

        if event.type == "move":
            pass


        else:
            pass

    def parse_draw(self, event):
        self.window.draw_char()

    def parse_clear(self, event):
        pass

    def parse_scroll(self, event):
        pass