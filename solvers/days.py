from typing import Any, Callable, Iterator

from .day01 import *
from .day02 import *
from .day03 import *
from .day04 import *
from .day05 import *

__all__ = ['SOLVER_LIST', 'SolverType']

type SolverType = Callable[[Iterator[str]], Iterator[Any]]

SOLVER_LIST: dict[int, tuple[str, SolverType]] = {
    1: ('Secret Entrance', solve01),
    2: ('Gift Shop', solve02),
    3: ('Lobby', solve03),
    4: ('Printing Department', solve04),
    5: ('Cafeteria', solve05)
}
