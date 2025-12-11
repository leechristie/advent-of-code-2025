from typing import Any, Callable, Iterator

from .day01 import *
from .day02 import *
from .day03 import *
from .day04 import *
from .day05 import *
from .day06 import *
from .day07 import *
from .day08 import *
from .day09 import *
from .day10 import *
from .day11 import *

__all__ = ['SOLVER_LIST', 'SolverType']

type SolverType = Callable[[Iterator[str]], Iterator[Any]] | Callable[[Iterator[str], Iterator[str] | None], Iterator[Any]]

SOLVER_LIST: dict[int, tuple[str, SolverType, bool]] = {
    1: ('Secret Entrance', solve01, False),
    2: ('Gift Shop', solve02, False),
    3: ('Lobby', solve03, False),
    4: ('Printing Department', solve04, False),
    5: ('Cafeteria', solve05, False),
    6: ('Trash Compactor', solve06, False),
    7: ('Laboratories', solve07, False),
    8: ('Playground', solve08, False),
    9: ('Movie Theater', solve09, False),
    # 10: ('Factory', solve10, False),
    11: ('Reactor', solve11, True)
}
