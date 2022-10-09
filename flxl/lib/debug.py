from os.path import dirname, isdir, join
from sys import modules


def is_debug_mode():
    if (
        isdir(join(dirname(modules['flxl'].__file__), '..', '.git'))
        and isdir('flxl')
    ):
        return True
    return False
