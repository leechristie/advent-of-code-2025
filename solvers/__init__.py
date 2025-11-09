import sys
import os
from typing import Any, Callable, Iterator

# list of solvers
from .day00 import *
type SolverType = Callable[[Iterator[str]], Iterator[Any]]
__SOLVER_LIST: list[tuple[str, SolverType]] = [
    ('Placeholder', solve00)
]


__all__ = ['solve']

# loads the required input file, and invokes the required solver
def solve(day: int | None=None, example: bool=False) -> int:

    # get the solver for the specified day
    if day is None:
        day = len(__SOLVER_LIST) - 1
    if not 0 <= day <= len(__SOLVER_LIST) - 1:
        print(f'no solver for day {day}', file=sys.stderr, end='\n', flush=True)
        return 1
    title: str
    solver: SolverType
    title, solver = __SOLVER_LIST[day]

    # print the header
    print('Advent of Code 2025')
    if example:
        print(f'Day {day} - {title} (Example Input)')
    else:
        print(f'Day {day} - {title}')

    # check that the required input file is available
    filename = f'input/{"example" if example else "input"}{day:02}.txt'
    if not os.path.exists(filename):
        print(f'missing file {filename}', file=sys.stderr, end='\n', flush=True)
        return 1

    try:

        with open(filename) as file:

            # pass the input file and get the first two yielded results
            active_solver = solver((line.strip('\n') for line in file))
            print(f'Part 1: ', flush=True)
            print(f'{next(active_solver)}', flush=True)
            print(f'Part 2: ', flush=True)
            print(f'{next(active_solver)}', flush=True)

            # solver should not yield a third result
            try:
                next(active_solver)
                print(flush=True)
                print(f'solver for day {day} yielded too many results', file=sys.stderr, end='\n', flush=True)
                return 1
            except StopIteration:
                pass

    except StopIteration:
        print(flush=True)
        print(f'solver for day {day} yielded too few results', file=sys.stderr, end='\n', flush=True)
        return 1

    return 0
