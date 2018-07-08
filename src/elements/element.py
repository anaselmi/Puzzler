import abc
import tdl

from consts import *


class Frame:
    def __init__(self, size=(0, 0), string="", plt=(..., ...)):
        self.size = self.width, self.height = size
        self.string = string
        self.plt = self.fg, self.bg = plt
        if self.width == 0 or self.height == 0:
            self.width = 0
            self.height = 0
            self.string = ""
            self.plt = (..., ...)

DEFAULT_FRAME = Frame(size=(1, 1), string=FRAME_STRING, plt=PLT_F)


class Element(abc.ABC):
    """Base class for UI elements.

    Wraps functionality around a TDL console, and adds attributes. Exposes methods that can
    be used by user code as determined by the name of the Element. Adds framing functionality"

    Notes:
        User code should not draw to con/win unless using a method exposed by a subclass of Element.

    Attributes:
        name (string): Used by outside code to determine specialized methods/attributes.
        size: Contains width and height of the element.
        con: The TDL console the element contains.
        win: The window of the console the element draws onto.
        plt: Foreground/Background colors of the element.
        frame: Frame used to frame the element.

    """
    def __init__(self, name, pos, size, plt=PLT_WB, frame=None):
        """Initializes element and optional frame.

        :param string name: Sets name for element.
        :param tuple pos: Sets default blit coordinates for console.
        :param tuple size: Size of the base console.
        :param tuple plt: Optional. Palette used by element.
        :param tuple frame: Optional. The framing surrounding the element.
        """
        self.name = name
        self.plt = self.fg, self.bg = plt
        self.updated = False
        self.rendered = False
        # Console.
        width, height = size
        self.con = tdl.Console(width, height)
        # Pos should be an attribute of the console, but Pycharm doesn't like it when I do that.
        self.pos = self.x, self.y = pos
        self.con.size = self.con.width, self.con.height
        self.con.set_colors(fg=self.fg, bg=self.bg)
        # Frame.
        if frame is None:
            frame = Frame()
        self.frame = frame
        self._draw_frame()
        # Window.
        width = self.con.width - (self.frame.width * 2)
        height = self.con.height - (self.frame.height * 2)
        self.win = tdl.Window(self.con, width=width, height=height, x=self.frame.width, y=self.frame.height)
        self.win.pos = self.win.x, self.win.y
        self.win.size = self.win.width, self.win.height

    def _draw_frame(self, frame=None):
        if frame is None:
            assert(hasattr(self, "frame"))
            frame = self.frame
        self.con.clear()
        self.con.draw_frame(x=0, y=0,
                            width=frame.width, height=frame.height,
                            string=frame.string, fg=frame.fg, bg=frame.bg)

    def render(self, screen):
        """ Given a screen to draw onto, the element blits itself at con.pos if it hasn't been rendered yet.

        :param screen:
        :return: None
        """
        if self.rendered:
            return
        x, y = self.pos
        screen.blit(self.con, x=x, y=y)
        self.rendered = True

    def reset(self):
        self.updated = False
        self.rendered = False

    def clear(self):
        """ Clears the contents of the element without clearing the frame.

        :return: None
        """
        self.win.clear()
        self.updated = False
        self.rendered = False

    def _adjust(self, pos):
        return pos[0] + self.frame.width, pos[1] + self.frame.height

    def in_elem(self, pos):
        """ Checks if a position is within the drawable portion of the screen.

        :param tuple pos: The position in question. (x, y).
        :return bool: Whether the position is in the usable part of the element or not.
        """
        x, y = pos
        if not (x >= 0 + self.frame.width) or not (x < self.con.width - self.frame.width):
            return False
        if not (y >= 0 + self.frame.height) or not (y < self.con.height - self.frame.height):
            return False
        return True
