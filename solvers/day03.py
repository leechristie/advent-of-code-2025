from typing import Iterator


def __max_joltage(bank: list[int], lower: int, bound: int, result: list[int], num_on: int) -> None:
    # can't speed up the current_digit check without slice because Python :/
    if num_on == 1:
        current_digit = max(bank[lower:bound])
        result.append(current_digit)
    else:
        current_digit = max(bank[lower:bound - num_on + 1])
        result.append(current_digit)
        position: int = bank.index(current_digit, lower)
        __max_joltage(bank, position + 1, bound, result, num_on - 1)


def max_joltage(bank: list[int], num_on: int) -> int:
    result: list[int] = []
    __max_joltage(bank, 0, len(bank), result, num_on)
    rv: int = 0
    for digit in result:
        rv *= 10
        rv += digit
    return rv


def solve03(lines: Iterator[str]) -> Iterator[int]:

    part1: int = 0
    part2: int = 0

    for line in lines:
        values: list[int] = [int(b) for b in line]
        part1 += max_joltage(values, 2)
        part2 += max_joltage(values, 12)

    yield part1
    assert 17321 == part1
    yield part2
    assert 171989894144198 == part2
