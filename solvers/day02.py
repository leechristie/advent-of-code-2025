from typing import Iterator
from printing.debug import print


def ranges(lines: Iterator[str]) -> Iterator[tuple[str, str]]:
    tokens = next(lines).split(',')
    for token in tokens:
        first, last = token.split('-')
        yield first, last


def all_ids_in_range(first: str, last: str) -> Iterator[str]:
    first_int = int(first)
    second_int = int(last)
    for product_id in range(first_int, second_int + 1):
        yield str(product_id)


def all_ids(lines: Iterator[str]) -> Iterator[str]:
    for first, last in ranges(lines):
        for product_id in all_ids_in_range(first, last):
            yield product_id


def solve02(lines: Iterator[str]) -> Iterator[int]:

    part1: int = 0
    part2: int = 0

    for product_id in all_ids(lines):
        if len(product_id) % 2 == 0:
            mid = len(product_id) // 2
            left, right = product_id[:mid], product_id[mid:]
            if left == right:
                part1 += int(product_id)

    yield part1
    yield part2
