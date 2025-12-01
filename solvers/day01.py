from typing import Iterator
from printing.debug import print

__all__ = ['solve01']

def solve01(lines: Iterator[str]) -> Iterator[int]:

    DIAL_NUMBERS: int = 100
    dial_position: int = 50

    part1: int = 0

    print(f'dial starts {dial_position}')
    for line in lines:
        direction: str = line[0]
        distance: int = int(line[1:])
        assert direction in ('L', 'R')
        dial_position += distance if direction == 'R' else -distance
        dial_position %= DIAL_NUMBERS
        if dial_position == 0:
            part1 += 1
        print(f'{direction}, {distance} dial at {dial_position}')

    yield part1

