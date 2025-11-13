import sys
from functools import partial
from typing import TextIO

from solvers.color import *

__PRINT = print

__all__ = ['print']

def print(*args, sep: str=' ', end: str='\n', file: TextIO=sys.stdout, flush: bool=True) -> None:
    color_print(*args, sep=sep, end=end, file=file, flush=flush, color=ASCII_GREEN)

