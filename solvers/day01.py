import time
from typing import Iterator
import random
from .debug import print

__all__ = ['solve01']

def solve01(file: Iterator[str]) -> Iterator[int]:

    part1: int = 0
    part2: int = 1

    # placeholder logic to test the correct file input01.txt or example01.txt is loaded
    for line in file:
        value: int = int(line)
        part1 += value
        part2 *= value

    time.sleep(random.randint(1, 10) / 10000)
    yield part1

    time.sleep(random.randint(1, 50) / 3000)  # sleep to test Part 1 gets output by `solve` before Part 2 is done
    yield part2
