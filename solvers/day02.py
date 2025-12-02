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


def is_repeat(product_id: str, sequence_length: int) -> bool:
    length: int = len(product_id)
    num_sequences: int = length // sequence_length
    sequence: str = product_id[:sequence_length]
    expected_sequence: str = sequence * num_sequences
    return product_id == expected_sequence


def cache_part2_potential_lengths(potential_sequence_lengths: list[list[int]], product_length: int) -> list[int]:
    while len(potential_sequence_lengths) <= product_length:
        potential_sequence_lengths.append([])
    potential: list[int] = potential_sequence_lengths[product_length]
    if not potential:
        for sequence_length in range(1, product_length // 2 + 1):
            if product_length % sequence_length == 0:
                potential.append(sequence_length)
    return potential


def solve02(lines: Iterator[str]) -> Iterator[int]:

    potential_sequence_lengths: list[list[int]] = []

    part1 = 0
    part2 = 0

    for first, last in ranges(lines):

        invalid_ids = set()
        product_length = len(first)
        potential = cache_part2_potential_lengths(potential_sequence_lengths, product_length)

        for sequence_length in potential:
            num_sequences: int = product_length // sequence_length
            first_prefix = int(first[:sequence_length])
            last_prefix = int(last[:sequence_length])
            for prefix in range(first_prefix, last_prefix + 1):
                expected_invalid_id: int = int(str(prefix) * num_sequences)
                if int(first) <= expected_invalid_id <= int(last):
                    if expected_invalid_id not in invalid_ids:
                        invalid_ids.add(expected_invalid_id)
                        part2 += expected_invalid_id
                    if num_sequences == 2:
                        part1 += expected_invalid_id

    yield part1
    yield part2
