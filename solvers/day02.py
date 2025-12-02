from itertools import product
from typing import Iterator

from mypy.checkexpr import defaultdict
from pygments.lexer import default

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
    num_sequences: int = length // sequence_length
    sequence: str = product_id[:sequence_length]
    expected_sequence: str = sequence * num_sequences
    return product_id == expected_sequence


def calc_max_check(product_id: str) -> int:
    if len(product_id) % 2 == 0:
        return len(product_id) // 2
    return len(product_id) // 3


def solve02(lines: Iterator[str]) -> Iterator[int]:

    part1: int = 0
    part2: int = 0

    all_ranges = list(ranges(lines))

    # lengths to check for part 2 (excludes half the length, which is checked separately)
    potential_sequence_lengths: list[list[int]] = []

    for first, last in all_ranges:
        for product_id in all_ids_in_range(first, last):

            is_invalid = False
            product_length = len(product_id)
            product_length_is_even = product_length % 2 == 0

            if product_length_is_even:
                if is_repeat(product_id, product_length // 2):
                    part1 += int(product_id)
                    is_invalid = True

            if not is_invalid and product_length > 2:

                # cache potential sequence lengths for part 2
                while len(potential_sequence_lengths) <= product_length - 3:
                    potential_sequence_lengths.append([])
                potential: list[int] = potential_sequence_lengths[product_length - 3]
                if not potential:
                    for sequence_length in range(1, product_length // 3 + 1):
                        if product_length % sequence_length == 0:
                            potential.append(sequence_length)

                # check potential sequence lengths (other than half the length)
                for sequence_length in potential:
                    if is_repeat(product_id, sequence_length):
                        is_invalid = True
                        break

            if is_invalid:
                part2 += int(product_id)

    yield part1
    assert (1227775554 == part1 or 64215794229 == part1)
    yield part2
    assert (4174379265 == part2 or 85513235135 == part2)
