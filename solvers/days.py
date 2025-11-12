from typing import Any, Callable, Iterator

from .day01 import *
from .day02 import *

__all__ = ['SOLVER_LIST', 'SolverType']

type SolverType = Callable[[Iterator[str]], Iterator[Any]]

SOLVER_LIST: dict[int, tuple[str, SolverType]] = {
    1: ('First Placeholder Day', solve01),
    2: ('Second Placeholder Day', solve02)
}
