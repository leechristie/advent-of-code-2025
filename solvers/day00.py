import time
from typing import Iterator

__all__ = ['solve00']

def solve00(file: Iterator[str]) -> Iterator[int]:

    part1: int = 0
    part2: int = 1

    # placeholder logic to test the correct file input00.txt or example00.txt is loaded
    for line in file:
        value: int = int(line)
        part1 += value
        part2 *= value

    time.sleep(1)
    yield part1

    time.sleep(3)  # sleep to test Part 1 gets output by `solve` before Part 2 is done
    yield part2
