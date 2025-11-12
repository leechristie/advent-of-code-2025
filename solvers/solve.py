from .days import *

import sys
import os
import time

__all__ = ['SolverError', 'solve', 'profile']


class SolverError(Exception):

    def __init__(self, *args):
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


def print_header(day: int, title: str, example: bool=False):
    print('Advent of Code 2025')
    if example:
        print(f'Day {day} - {title} (Example Input)')
    else:
        print(f'Day {day} - {title}')


def load_input_file(day: int | None=None, example: bool=False):
    filename = f'input/{"example" if example else "input"}{day:02}.txt'
    try:
        return open(filename)
    except FileNotFoundError:
        raise SolverError(f'missing input file {filename}')


# loads the required input file, and invokes the required solver
def solve(day: int | None=None, example: bool=False) -> None:
    day, title, solver = get_solver_for(day)
    print_header(day, title, example)
    try:
        with load_input_file(day, example) as file:

            # pass the input file and get the first two yielded results
            active_solver = solver((line.strip('\n') for line in file))
            try:
                print(f'Part 1: {next(active_solver)}', flush=True)
            except TypeError as err:
                if 'is not an iterator' in str(err):
                    raise SolverError(f'solver for day {day} did not yield any results')
                raise
            print(f'Part 2: {next(active_solver)}', flush=True)

            # solver should not yield a third result
            try:
                next(active_solver)
                raise SolverError(f'solver for day {day} yielded too many results')
            except StopIteration:
                pass

    except StopIteration:
        raise SolverError(f'solver for day {day} yielded too few results')


def profile_single(day, solver, samples: int):
    start = time.perf_counter()
    for _ in range(samples):
        with load_input_file(day, example=False) as file:
            active_solver = solver((line.strip('\n') for line in file))
            assert (len(list(active_solver)) == 2), f'solver for day {day} did not return 2 results in profile'
    average_time = (time.perf_counter() - start) / samples
    return average_time


def align_decimal(value: float, leading_figures, decimal_places: int):
    formatted = f'{value:.{decimal_places}f}'
    actual_leading_figures = len(formatted) - 1 - decimal_places
    assert (actual_leading_figures <= leading_figures), f'cannot format decimal {value} as specified'
    formatted = ' ' * (leading_figures - actual_leading_figures) + formatted
    return formatted


def print_table_header(max_title: int, leading_figures: int, decimal_places: int):
    print(f'| Day | {'Title':<{max_title}} | {'Runtime':>{leading_figures + decimal_places + 5}} |')
    print(f'|-----|{'-' * (max_title + 2)}|{'-' * (leading_figures + decimal_places + 5 + 2)}|')


def profile(samples: int):
    print(f'profiling all solvers with {samples} samples . . ')
    print()
    max_title = max(len(title) for title, _ in SOLVER_LIST.values())
    print_table_header(max_title, 4, 6)
    for day in sorted(SOLVER_LIST.keys()):
        day, title, solver = get_solver_for(day)
        average_time = profile_single(day, solver, samples)
        print(f'| {day:>3} | {title:<{max_title}} | {align_decimal(average_time, 4, 6)} sec |')
