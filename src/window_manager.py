import tdl
import tcod

# TODO
class WindowManager:
    def __init__(self, root):
        self.root = root
        pass

    def message_init(self):
        self.message_end = 0
        return tdl.Window(root, 0, 0, None, self.message_end)

    def game_init(self):
        return tdl.Window(root, )

