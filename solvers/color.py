import sys
from typing import TextIO

__PRINT = print

__all__ = ['color_print', 'ASCII_RED', 'ASCII_GREEN', 'ASCII_YELLOW', 'ASCII_LIGHT_PURPLE', 'ASCII_PURPLE', 'ASCII_CYAN']

ASCII_RED: int = 91
ASCII_GREEN: int = 92
ASCII_YELLOW: int = 93
ASCII_LIGHT_PURPLE: int = 94
ASCII_PURPLE: int = 95
ASCII_CYAN: int = 96


def color_print(*args, sep: str=' ', end: str='\n', file: TextIO=sys.stdout, flush: bool=True, color: int | None=None) -> None:
    if color is not None:
        __PRINT(f'\033[{color}m{sep.join((str(a) for a in args))}\033[00m', sep='', end=end, file=file, flush=flush)
    else:
        __PRINT(f'{color}{sep.join((str(a) for a in args))}', sep='', end=end, file=file, flush=flush)
