from typing import Any, Callable, Iterator

from .day01 import *

__all__ = ['SOLVER_LIST', 'SolverType']

type SolverType = Callable[[Iterator[str]], Iterator[Any]]

SOLVER_LIST: dict[int, tuple[str, SolverType]] = {
    1: ('Secret Entrance', solve01)
}
