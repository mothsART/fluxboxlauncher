import sys
from os.path import dirname, isdir, join


def is_debug_mode():
    d = dirname(sys.modules['flxl'].__file__)
    if isdir(join(d, '..', '.git')):
        return True
    return False
