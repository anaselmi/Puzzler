from ecs_classes import ComponentABC
from consts import *


class RenderComponent(ComponentABC):

    def __init__(self, **kwargs):
        priority = 0
        super().__init__(priority, **kwargs)

    @classmethod
    def allowed_events(cls):
        return ["draw", "clear", "scroll"]

    @classmethod
    def allowed_tags(cls):
        return {"x": int, "y": int, "char": str, "fg": tuple, "bg": tuple, "active": bool}

    def parse(self, event):
        if not self.active:
            return None

        if event.type == "draw":
            self.parse_draw(event)

        elif event.type == "clear":
            self.parse_clear(event)

        elif event.type == "scroll":
            self.parse_scroll(event)

        else:
            pass

    def parse_draw(self, event):
        pass

    def parse_clear(self, event):
        pass

    def parse_scroll(self, event):
        pass


Bob = RenderComponent(x=0, y=0, char="@", fg=RED, bg=BLACK, active=True)
