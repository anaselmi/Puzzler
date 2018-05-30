import tdl

from consts import *


class Element:
    """Base class for UI elements.

    Creates and adds framing functionality to a TDL console. Exposes methods that users can
    use in predefined ways they determine from the name of the element."

    Notes:
        Do not draw onto the console outside of methods provided by class and subclasses.

    Attributes:
        name (string): Used by outside code to determine specialized methods/attributes.
        size: Contains width and height.
        w (int): Width of the element.
        h (int): Height of the element.
        c: A TDL console the element draws onto.
        c_pos: Contains c_x and c_y.
        c_x (int): X position of the console relative to the screen.
        c_y (int): Y position of the console relative to the screen.
        c_size: Contains c_width and c_height.
        c_w (int): Width of the console.
        c_h (int): Height of the console.
        fg: Default color of characters drawn inside the element.
        bg: Default background color of the element.
        f_size: Contains f_w and f_h.
        f_w (int): Width of the frame.
        f_h (int): Height of the frame.
        f_char (string): Character used to draw the frame.
        f_fg: Color of the frame character.
        f_bg: Background color of the frame.
    """
    def __init__(self, name, pos, size, sc_size, plt=PLT_WB, f_size=F_SIZE, f_char=F_CHAR, f_plt=(..., ...)):
        """Initializes element and optional frame.

        :param string name: Sets name for element.
        :param tuple pos: Sets default blit coordinates for console (takes frame into account).
        :param tuple size: Size of the base console. A value of -1 causes that dimension to fill the screen.
        :param tuple sc_size: Size of the screen.
        :param tuple plt: Palette used by element.
        :param tuple f_size: Size of the frame.
        :param tuple f_char: Character used to frame element.
        :param tuple f_plt: Palette used by frame.
        """
        super().__init__()
        self.name = name
        self.c_pos = self.c_x, self.c_y = pos
        self._init_console(size, sc_size, plt)
        self._init_frame(f_size, f_char, f_plt)

    def _init_console(self, size, screen_size, plt):
        width, height = size
        screen_width, screen_height = screen_size
        self.c_w = screen_width if width == -1 else width
        self.c_h = screen_height if height == -1 else height
        self.c_size = self.c_w, self.c_h
        self.c = tdl.Console(self.c_w, self.c_h)
        self.plt = self.fg, self.bg = plt
        self.c.set_colors(fg=self.fg, bg=self.bg)

    def _init_frame(self, size, char, plt):
        self.f_size = self.f_w, self.f_h = size
        self.f_char = char
        self.f_plt = self.f_fg, self.f_bg = plt
        if self.f_w == 0 or self.f_h == 0:
            self._draw_frame((0, 0), "", (..., ...))
        else:
            self._draw_frame(self.f_size, self.f_char, self.f_plt)
        self.w = self.c_w - (self.f_w * 2)
        self.h = self.c_h - (self.f_h * 2)
        self.size = self.w, self.h

    def clear(self):
        """Clears the element. Does not clear the frame.

        :return: None
        """
        self.c.draw_rect(self.f_w, self.f_h, self.w, self.h, None)

    def _draw_frame(self, size, char, plt):
        width, height = size
        fg, bg = plt
        self.c.draw_rect(0, 0,
                         width=width, height=height,
                         string=char, fg=fg, bg=bg)

    def _adjust(self, pos):
        x, y = pos
        adjusted = x + self.f_w, y + self.f_h
        return adjusted

    def in_elem(self, pos):
        """ Checks if a position is within the drawable portion of the screen.

        :param tuple pos: The position in question. (x, y).
        :return bool: Whether the position is in the usable part of the element or not.
        """
        x, y = pos
        if not (x >= 0 + self.f_w) or not (x < self.w - self.f_w):
            return False
        if not (y >= 0 + self.f_h) or not (y < self.h - self.f_h):
            return False
        return True
