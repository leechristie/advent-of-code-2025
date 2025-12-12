from enum import Enum
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
from .day12 import *

__all__ = ['SOLVER_LIST', 'Solver', 'SolverWithTwoExampleInputs', 'NumberOfExampleInputs', 'SolvedState']


type Solver = Callable[
    [Iterator[str]],
    Iterator[Any]
]


type SolverWithTwoExampleInputs = Callable[
    [Iterator[str], Iterator[str]],
    Iterator[Any]
]


class NumberOfExampleInputs(Enum):
    SINGLE = 1
    SEPARATE_EXAMPLES = 2
SINGLE: NumberOfExampleInputs = NumberOfExampleInputs.SINGLE
SEPARATE_EXAMPLES: NumberOfExampleInputs = NumberOfExampleInputs.SEPARATE_EXAMPLES


class SolvedState(Enum):
    SOLVED = 1
    UNSOLVED = 2
SOLVED: SolvedState = SolvedState.SOLVED
UNSOLVED: SolvedState = SolvedState.UNSOLVED


SOLVER_LIST: dict[int, tuple[str, Solver | SolverWithTwoExampleInputs, NumberOfExampleInputs, SolvedState]] = {
    1:  ('Secret Entrance',     solve01, SINGLE,            SOLVED),
    2:  ('Gift Shop',           solve02, SINGLE,            SOLVED),
    3:  ('Lobby',               solve03, SINGLE,            SOLVED),
    4:  ('Printing Department', solve04, SINGLE,            SOLVED),
    5:  ('Cafeteria',           solve05, SINGLE,            SOLVED),
    6:  ('Trash Compactor',     solve06, SINGLE,            SOLVED),
    7:  ('Laboratories',        solve07, SINGLE,            SOLVED),
    8:  ('Playground',          solve08, SINGLE,            SOLVED),
    9:  ('Movie Theater',       solve09, SINGLE,            SOLVED),
    10: ('Factory',             solve10, SINGLE,            UNSOLVED),
    11: ('Reactor',             solve11, SEPARATE_EXAMPLES, SOLVED),
    12: ('Christmas Tree Farm', solve12, SINGLE,            UNSOLVED)
}
