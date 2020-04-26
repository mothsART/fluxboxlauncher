from os.path import dirname, join, isdir
import sys


def is_debug_mode():
    d = dirname(sys.modules["flxl"].__file__)
    if isdir(join(d, '..', '.git')):
        return True
    return False
