import tdl
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
    def default_tags(cls):
        return {"x": None, "y": None, "char": "C", "fg": WHITE, "bg": BLACK, "active": True, width: None}

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
        self.window.draw_char()

    def parse_clear(self, event):
        pass

    def parse_scroll(self, event):
        pass

PlayerRender = RenderComponent(x=0, y=0, char="@", fg=RED, bg=BLACK, active=True)


class MoveComponent(ComponentABC):

    def __init__(self, **kwargs):
        priority = 1
        super().__init__(priority, **kwargs)

    @classmethod
    def allowed_events(cls):
        return ["draw", "clear", "scroll"]

    @classmethod
    def allowed_tags(cls):
        return {"speed": int, "direction": str, "active": bool}

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
        self.window.draw_char()

    def parse_clear(self, event):
        pass

    def parse_scroll(self, event):
        pass