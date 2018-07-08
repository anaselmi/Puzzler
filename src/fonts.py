class Font:
    def __init__(self, path, size, greyscale, alt_layout):
        self.path = path
        self.size = size
        self.greyscale = greyscale
        self.alt_layout = alt_layout

Courier12 = Font(path="assets\\courier12x12.png", size=12, greyscale=True, alt_layout=True)
