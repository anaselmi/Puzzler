import sys
from io import StringIO
from tdl import Console

# Ultimately this file will get split up into multiple components if/when it gets large enough
class NullIO(StringIO):
    def write(self, txt):
        pass


def silence(fn):
    """Decorator to silence functions/methods."""
    # Useful for silencing TDL when it creates the root console
    def silent_wrapper(*args, **kwargs):
        saved_stdout = sys.stdout
        sys.stdout = NullIO()
        result = fn(*args, **kwargs)
        sys.stdout = saved_stdout
        return result
    return silent_wrapper


# Not sure what naming convention this should follow because it's a function, but it returns an object
# If you want, you can pretend it's CamelCase
@silence
def silent_console(width, height):
        return Console(width, height)
