from typing import Iterator

import numpy as np


__all__ = ['solve06']


def parse_problems_part1(lines: list[str]) -> tuple[int, np.ndarray, list[str]]:
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
    num_problems, number_grid, operators = parse_problems_part1(lines)
    rv: int = 0
    for i in range(num_problems):
        numbers = number_grid[:,i]
        operator = operators[i]
        solution = (numbers.sum() if operator == '+' else numbers.prod()).item()
        rv += solution
    return rv


def transpose_lines(lines: list[str]) -> list[str]:
    num_rows: int = len(lines)
    num_cols: int = len(lines[0])
    transposed_orientation: list[list[str]] = [ [''] * num_rows for _ in range(num_cols)]
    for row, line in enumerate(lines):
        for col, character in enumerate(line):
            transposed_orientation[col][row] = character
    return [''.join(line) for line in transposed_orientation]


def part2_total(lines: list[str]) -> int:
    rv: int = 0
    multiply: bool = False
    running_sum_or_product: int = -1
    for line in lines:
        num_str, op_str = line[:-1].strip(' '), line[-1]
        if op_str == '*':
            multiply = True
        elif op_str == '+':
            multiply = False
        else:
            assert op_str == ' '
        if num_str:
            if multiply:
                running_sum_or_product = int(num_str) if running_sum_or_product == -1 else running_sum_or_product * int(num_str)
            else:
                running_sum_or_product = int(num_str) if running_sum_or_product == -1 else running_sum_or_product + int(num_str)
        else:
            rv += running_sum_or_product
            running_sum_or_product = -1
    assert running_sum_or_product != -1
    rv += running_sum_or_product
    return rv


def solve06(lines: Iterator[str]) -> Iterator[int]:

    normal: list[str] = list(lines)
    transposed: list[str] = transpose_lines(normal)

    part1: int = part1_total(normal)
    yield part1

    part2: int = part2_total(transposed)
    yield part2
