from typing import Iterator
from printing.debug import print


__all__ = ['solve05']


def parse_fresh_ranges(lines: Iterator[str]) -> list[tuple[int, int]]:
    rv: list[tuple[int, int]] = []
    for line in lines:
        if not line:
            return rv
        lower, upper = line.split('-')
        rv.append((int(lower), int(upper)))
    raise AssertionError('bad input file')


def parse_ingredients(lines: Iterator[str]) -> Iterator[int]:
    for line in lines:
        yield int(line)


def if_in_fresh_range(ingredient: int, fresh_range: tuple[int, int]) -> bool:
    return fresh_range[0] <= ingredient <= fresh_range[1]


def is_fresh(ingredient: int, fresh_ranges: list[tuple[int, int]]) -> bool:
    for fresh_range in fresh_ranges:
        if if_in_fresh_range(ingredient, fresh_range):
            return True
    return False


def number_of_fresh_ingredients(lines: Iterator[str], fresh_ranges: list[tuple[int, int]]) -> int:
    fresh_count: int = 0
    for ingredient in parse_ingredients(lines):
        if is_fresh(ingredient, fresh_ranges):
            fresh_count += 1
    return fresh_count


def number_of_fresh_ingredient_ids(fresh_ranges: list[tuple[int, int]]) -> int:
    return 0


def solve05(lines: Iterator[str]) -> Iterator[int]:

    fresh_ranges: list[tuple[int, int]] = parse_fresh_ranges(lines)

    yield number_of_fresh_ingredients(lines, fresh_ranges)
    yield number_of_fresh_ingredient_ids(fresh_ranges)
