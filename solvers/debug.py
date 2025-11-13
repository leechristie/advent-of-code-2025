from functools import partial

from solvers.color import *

__PRINT = print

__all__ = ['print']

print = partial(color_print, color=ASCII_GREEN)
