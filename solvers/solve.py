from functools import partial
from io import TextIOWrapper
import time
from typing import TextIO, cast

from printing.color import color_print, ASCII_YELLOW
from .days import *

__all__ = ['SolverError', 'solve_all', 'solve', 'profile']


class SolverError(Exception):

    def __init__(self, *args) -> None:
        super().__init__(*args)


def get_solver_for(day: int | None=None) -> tuple[int, str, Solver | SolverWithTwoExampleInputs, NumberOfExampleInputs, SolvedState]:
    if not SOLVER_LIST:
        raise SolverError('no solvers found')
    if day is None:
        day = max(SOLVER_LIST)
    if day not in SOLVER_LIST:
        raise SolverError(f'no solver for day {day}')
    title, solver, has_example_b, is_solved = SOLVER_LIST[day]
    return day, title, solver, has_example_b, is_solved


def print_header(day: int, title: str, example: bool=False) -> None:
    print('Advent of Code 2025')
    print(f'Day {day} - {title}')
    if example:
        color_print(f'currently using example input file', color=ASCII_YELLOW)


def load_input_file(day: int | None=None, example: bool=False, example_b: bool=False) -> TextIOWrapper:
    if not example:
        assert (not example_b), f'cannot load example b, if not using example'
    if not example_b:
        filename = f'input/2025/{"example" if example else "input"}{day:02}.txt'
    else:
        filename = f'input/2025/example{day:02}b.txt'
    try:
        return open(filename)
    except FileNotFoundError:
        raise SolverError(f'missing input file {filename}')


def solve_all() -> None:
    for day, (_, _, _, solved_state) in SOLVER_LIST.items():
        if solved_state == SolvedState.SOLVED:
            print()
            solve(day, example=False)


def solve(day: int | None=None, example: bool=False) -> None:
    day, title, solver, number_of_example_inputs, _ = get_solver_for(day)
    use_example_b: bool = example and number_of_example_inputs == NumberOfExampleInputs.SEPARATE_EXAMPLES
    print_header(day, title, example)
    try:
        example_b_file: TextIO | None = None
        if use_example_b:
            example_b_file = load_input_file(day, example, True)
        with load_input_file(day, example) as file:

            if example_b_file is not None:
                solver = cast(SolverWithTwoExampleInputs, solver)
                active_solver = solver((line.strip('\n') for line in file), (line.strip('\n') for line in example_b_file))
            else:
                solver = cast(Solver, solver)
                active_solver = solver((line.strip('\n') for line in file))
            if not hasattr(active_solver, '__next__'):
                raise SolverError(f'solver for day {day} did not yield any results')

            print_result = partial(color_print, color=ASCII_YELLOW) if example else print

            start: float = time.perf_counter()

            part1 = next(active_solver)
            print('Part 1: ', end='', flush=True)
            print_result(part1, end='\n', flush=True)

            part2 = next(active_solver)
            print('Part 2: ', end='', flush=True)
            print_result(part2, end='\n', flush=True)

            single_time: float = time.perf_counter() - start

            print('Time : ', end='', flush=True)
            print_result(f'{single_time:.6f} sec', end='\n', flush=True)

            try:
                next(active_solver)
                if example_b_file is not None:
                    example_b_file.close()
                    example_b_file = None
                raise SolverError(f'solver for day {day} yielded too many results')
            except StopIteration:
                pass

    except StopIteration:
        if example_b_file is not None:
            example_b_file.close()
            example_b_file = None
        raise SolverError(f'solver for day {day} yielded too few results')


def samples_for_single_time(single_time: float) -> int:
    if single_time > 1:
        return 3
    if single_time > 0.1:
        return 30
    if single_time > 0.01:
        return 300
    if single_time > 0.001:
        return 3000
    if single_time > 0.0_001:
        return 30_000
    if single_time > 0.00_001:
        return 300_000
    if single_time > 0.000_001:
        return 3_000_000
    if single_time > 0.0_000_001:
        return 30_000_000
    return 300_000_000


def profile_single_pre_loaded(day: int, solver: Solver) -> tuple[float, int]:

    with load_input_file(day, example=False) as file:
        lines = [line.strip('\n') for line in file]

    # warm up run
    _ = list(solver(iter(lines)))

    # run once to determine sample count
    start: float = time.perf_counter()
    _ = list(solver(iter(lines)))
    single_time = time.perf_counter() - start
    samples: int = samples_for_single_time(single_time)

    # profiling
    start = time.perf_counter()
    for _ in range(samples):
        active_solver = solver(iter(lines))
        assert (len(list(active_solver)) == 2), f'solver for day {day} did not return 2 results in profile'
    average_time: float = (time.perf_counter() - start) / samples
    return average_time * 1000.0, samples


def align_decimal(value: float, leading_figures, decimal_places: int) -> str:
    formatted = f'{value:.{decimal_places}f}'
    actual_leading_figures = len(formatted) - 1 - decimal_places
    assert (actual_leading_figures <= leading_figures), f'cannot format decimal {value} as specified'
    return ' ' * (leading_figures - actual_leading_figures) + formatted


def print_profile_header( max_title: int, leading_figures: int, decimal_places: int) -> None:
    print(f'profiling all solvers . . ')
    print()
    print(f'| Day | {'Title':<{max_title}} | {'Runtime':>{leading_figures + decimal_places + 4}} | Samples Run |')
    print(f'|-----|{'-' * (max_title + 2)}|{'-' * (leading_figures + decimal_places + 5 + 1)}|-------------|')


def print_profile_row(day: int, title: str, max_title: int, average_time: float, samples: int, leading_figures: int, decimal_places: int) -> None:
    print(f'| {day:>3} | {title:<{max_title}} | {align_decimal(average_time, leading_figures, decimal_places)} ms | {samples:>11,} |')


def profile() -> None:
    max_title = max(len(title) for title, _, _, is_solved in SOLVER_LIST.values())
    print_profile_header(max_title, 9, 2)
    for day in sorted(SOLVER_LIST.keys()):
        day, title, solver, _, is_solved = get_solver_for(day)
        if is_solved == SolvedState.UNSOLVED:
            continue
        solver = cast(Solver, solver)
        average_time, samples = profile_single_pre_loaded(day, solver)
        print_profile_row(day, title, max_title, average_time, samples, 9, 2)
