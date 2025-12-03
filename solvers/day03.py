from typing import Iterator


def __max_joltage(bank: list[int], lower: int, bound: int, result: int, num_on: int) -> int:

    # final digit to choose
    if num_on == 1:
        current_digit = max(bank[lower:bound])  # can't speed up  without slice because Python :/
        return result * 10 + current_digit

    current_digit = max(bank[lower:bound - num_on + 1])  # can't speed up without slice because Python :/
    position: int = bank.index(current_digit, lower)
    return __max_joltage(bank, position + 1, bound, result * 10 + current_digit, num_on - 1)


def max_joltage(bank: list[int], num_on: int) -> int:
    return __max_joltage(bank, 0, len(bank), 0, num_on)


def solve03(lines: Iterator[str]) -> Iterator[int]:

    part1: int = 0
    part2: int = 0

    for line in lines:
        values: list[int] = [int(b) for b in line]
        part1 += max_joltage(values, 2)
        part2 += max_joltage(values, 12)

    yield part1
    yield part2
