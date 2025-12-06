from typing import Iterator

import numpy as np


__all__ = ['solve06']


def parse_problems(lines: list[str]) -> tuple[int, np.ndarray, list[str]]:
    number_grid: list[list[int]] = []
    for line in lines:
        line = line.strip(' ')
        while '  ' in line:
            line = line.replace('  ', ' ')
        line_split = line.split(' ')
        if line_split[0] in '*+':
            num_problems: int = len(line_split)
            return num_problems, np.array(number_grid, dtype=np.int16), line_split
        number_grid.append([int(e) for e in line_split])
    raise AssertionError('bad input file')


def part1_total(lines: list[str]) -> int:
    num_problems: int
    numbers: np.ndarray
    operators: list[str]
    num_problems, number_grid, operators = parse_problems(lines)
    rv: int = 0
    for i in range(num_problems):
        numbers = number_grid[:,i]
        operator = operators[i]
        solution = (numbers.sum() if operator == '+' else numbers.prod()).item()
        rv += solution
    return rv


def is_slice_point(lines: list[str], slice_point: int) -> bool:
    for line in lines:
        if line[slice_point] != ' ':
            return False
    return True


def find_ranges(lines: list[str]) -> list[tuple[int, int]]:
    line_length: int = len(lines[0])
    rv: list[tuple[int, int]] = []
    for slice_point in range(line_length):
        if is_slice_point(lines, slice_point):
            if not rv:
                rv.append((0, slice_point))
            else:
                rv.append((rv[-1][1] + 1, slice_point))
    rv.append((rv[-1][1] + 1, line_length))
    return rv


def extract_range(lines: list[str], lower: int, bound: int) -> tuple[list[str], str]:
    rv: list[str] = []
    for line in lines:
        rv.append(line[lower:bound].replace(' ', ' '))
    return rv[:-1], rv[-1].strip(' ')


def formatted_numbers_to_grid(formatted_numbers: list[str]) -> np.ndarray:
    numbers: list[list[int]] = []
    for line in formatted_numbers:
        numbers.append([int(d) for d in line.replace(' ', '0')])
    rv: np.ndarray = np.array(numbers, dtype=np.int8)
    return rv.transpose()


def part2_total(lines: list[str]) -> int:
    rv: int = 0
    ranges: list[tuple[int, int]] = find_ranges(lines)
    formatted_numbers: list[str]
    operator: str
    for lower, bound in ranges:
        formatted_numbers, operator = extract_range(lines, lower, bound)
        grid: np.ndarray = formatted_numbers_to_grid(formatted_numbers)
        numbers_items: list[int] = []
        for row in grid:
            row_str: str = ''.join([str(d) for d in row]).strip('0')
            row_value: int = int(row_str)
            numbers_items.append(row_value)
        numbers: np.ndarray = np.array(numbers_items, dtype=np.int16)
        solution = (numbers.sum() if operator == '+' else numbers.prod()).item()
        rv += solution
    return rv


def solve06(lines: Iterator[str]) -> Iterator[int]:

    lines_copy: list[str] = list(lines)

    part1: int = part1_total(lines_copy)
    yield part1

    part2: int = part2_total(lines_copy)
    yield part2
