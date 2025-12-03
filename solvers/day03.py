from typing import Iterator


# slow recursive implementation, to fix
def __max_joltage_slow(bank: list[int], num_on: int, previous_on: list[int]) -> list[int]:
    exclusion: int = - (num_on - 1)
    if num_on == 2:
        assert exclusion == -1
    if exclusion == 0:
        look_in = bank
    else:
       look_in: list[int] = bank[:exclusion]
    current_digit: int = max(look_in)
    next_offset: int = bank.index(current_digit) + 1
    if num_on == 1:
        return previous_on + [current_digit]
    return __max_joltage_slow(bank[next_offset:], num_on-1, previous_on + [current_digit])


def __max_joltage_fast(bank: list[int], lower: int, bound: int, result: list[int]) -> None:
    pass  # TODO - still working on this version


def max_joltage(bank: list[int], num_on: int) -> int:
    return int(''.join((str(d) for d in __max_joltage_slow(bank, num_on, []))))
    # result: list[int] = []
    # __max_joltage_fast(bank, 0, len(bank), result)
    # rv: int = 0
    # for digit in result:
    #     rv *= 10
    #     rv += digit
    # return rv


def solve03(lines: Iterator[str]) -> Iterator[int]:

    part1: int = 0
    part2: int = 0

    for line in lines:
        values: list[int] = [int(b) for b in line]
        part1 += max_joltage(values, 2)
        part2 += max_joltage(values, 12)

    yield part1
    yield part2

    # 3.7 ms before optimising
