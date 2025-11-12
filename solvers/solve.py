import sys
from io import TextIOWrapper

from .days import *

import time

__all__ = ['SolverError', 'solve', 'profile']


class SolverError(Exception):

    def __init__(self, *args) -> None:
        super().__init__(*args)


def get_solver_for(day: int | None=None) -> tuple[int, str, SolverType]:
    if not SOLVER_LIST:
        raise SolverError('no solvers found')
    if day is None:
        day = max(SOLVER_LIST)
    if day not in SOLVER_LIST:
        raise SolverError(f'no solver for day {day}')
    title, solver = SOLVER_LIST[day]
    return day, title, solver


def print_header(day: int, title: str, example: bool=False) -> None:
    print('Advent of Code 2025')
    print(f'Day {day} - {title}')
    if example:
        time.sleep(0.01)
        print(f'currently using example input file', file=sys.stderr, end='\n', flush=True)
        time.sleep(0.01)


def load_input_file(day: int | None=None, example: bool=False) -> TextIOWrapper:
    filename = f'input/{"example" if example else "input"}{day:02}.txt'
    try:
        return open(filename)
    except FileNotFoundError:
        raise SolverError(f'missing input file {filename}')


def solve(day: int | None=None, example: bool=False) -> None:
    day, title, solver = get_solver_for(day)
    print_header(day, title, example)
    try:
        with load_input_file(day, example) as file:

            active_solver = solver((line.strip('\n') for line in file))
            if not hasattr(active_solver, '__next__'):
                raise SolverError(f'solver for day {day} did not yield any results')

            print(f'Part 1: {next(active_solver)}', flush=True)
            print(f'Part 2: {next(active_solver)}', flush=True)

            try:
                next(active_solver)
                raise SolverError(f'solver for day {day} yielded too many results')
            except StopIteration:
                pass

    except StopIteration:
        raise SolverError(f'solver for day {day} yielded too few results')


def profile_single(day: int, solver: SolverType, samples: int) -> float:
    start: float = time.perf_counter()
    for _ in range(samples):
        with load_input_file(day, example=False) as file:
            active_solver = solver((line.strip('\n') for line in file))
            assert (len(list(active_solver)) == 2), f'solver for day {day} did not return 2 results in profile'
    average_time: float = (time.perf_counter() - start) / samples
    return average_time


def align_decimal(value: float, leading_figures, decimal_places: int) -> str:
    formatted = f'{value:.{decimal_places}f}'
    actual_leading_figures = len(formatted) - 1 - decimal_places
    assert (actual_leading_figures <= leading_figures), f'cannot format decimal {value} as specified'
    return ' ' * (leading_figures - actual_leading_figures) + formatted


def print_profile_header(samples: int, max_title: int, leading_figures: int, decimal_places: int) -> None:
    print(f'profiling all solvers with {samples} samples . . ')
    print()
    print(f'| Day | {'Title':<{max_title}} | {'Runtime':>{leading_figures + decimal_places + 5}} |')
    print(f'|-----|{'-' * (max_title + 2)}|{'-' * (leading_figures + decimal_places + 5 + 2)}|')


def print_profile_row(day: int, title: str, max_title: int, average_time: float, leading_figures: int, decimal_places: int) -> None:
    print(f'| {day:>3} | {title:<{max_title}} | {align_decimal(average_time, leading_figures, decimal_places)} sec |')


def profile(samples: int) -> None:
    max_title = max(len(title) for title, _ in SOLVER_LIST.values())
    print_profile_header(samples, max_title, 3, 6)
    for day in sorted(SOLVER_LIST.keys()):
        day, title, solver = get_solver_for(day)
        average_time = profile_single(day, solver, samples)
        print_profile_row(day, title, max_title, average_time, 3, 6)
