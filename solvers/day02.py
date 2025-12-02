from itertools import product
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




def is_repeat(product_id: str, sequence_length: int) -> bool:
    length: int = len(product_id)
    if length % sequence_length != 0:
        return False
    num_sequences: int = length // sequence_length
    expected_sequence = product_id[:sequence_length] * num_sequences
    return product_id == expected_sequence



def calc_max_check(product_id: str) -> int:
    if len(product_id) % 2 == 0:
        return len(product_id) // 2
    return len(product_id) // 3


def solve02(lines: Iterator[str]) -> Iterator[int]:

    part1: int = 0
    part2: int = 0

    all_ranges = list(ranges(lines))

    for first, last in all_ranges:
        for product_id in all_ids_in_range(first, last):
            is_invalid_part1 = False
            is_invalid_part2 = False
            product_length = len(product_id)
            product_length_is_even = product_length % 2 == 0
            sequence_length_bound = (product_length // 2 + 1) if product_length_is_even else (product_length // 3 + 1)
            for sequence_length in range(1, sequence_length_bound):
                if is_repeat(product_id, sequence_length):
                    if product_length_is_even and sequence_length == product_length // 2:
                        is_invalid_part1 = True
                    is_invalid_part2 = True
            if is_invalid_part1:
                part1 += int(product_id)
            if is_invalid_part2:
                part2 += int(product_id)

    yield part1
    assert (1227775554 == part1 or 64215794229 == part1)
    yield part2
    assert (4174379265 == part2 or 85513235135 == part2)
