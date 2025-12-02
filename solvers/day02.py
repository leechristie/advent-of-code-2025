from typing import Iterator

from printing.debug import print


def ranges(lines: Iterator[str]) -> Iterator[tuple[str, str]]:
    tokens = next(lines).split(',')
    for token in tokens:
        first, last = token.split('-')
        if len(first) == len(last):
            yield first, last
        else:
            # split the range if different lengths
            yield first, '9' * len(first)       # xxx to 999
            yield '1' + '0' * len(first), last  # 1000 to yyyy


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


def cache_part2_potential_lengths(potential_sequence_lengths: list[list[int]], product_length: int) -> list[int]:
    while len(potential_sequence_lengths) <= product_length:
        potential_sequence_lengths.append([])
    potential: list[int] = potential_sequence_lengths[product_length]
    if not potential:
        for sequence_length in range(1, product_length // 2 + 1):  # was // 3
            if product_length % sequence_length == 0:
                potential.append(sequence_length)
    return potential


def solve02(lines: Iterator[str]) -> Iterator[int]:

    potential_sequence_lengths: list[list[int]] = []

    invalid_ids = set()
    part1 = 0

    for first, last in ranges(lines):

        product_length = len(first)

        potential = cache_part2_potential_lengths(potential_sequence_lengths, product_length)

        for sequence_length in potential:
            num_sequences: int = product_length // sequence_length
            first_prefix = int(first[:sequence_length])
            last_prefix = int(last[:sequence_length])
            for prefix in range(first_prefix, last_prefix + 1):
                expected_invalid_id: int = int(str(prefix) * num_sequences)
                if int(first) <= expected_invalid_id <= int(last):
                    invalid_ids.add(expected_invalid_id)
                    if num_sequences == 2:
                        part1 += expected_invalid_id

    yield part1
    # assert part1 == 64215794229

    yield sum(invalid_ids)
    # assert sum(invalid_ids) == 85513235135
