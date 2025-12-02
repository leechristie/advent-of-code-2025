from typing import Iterator

__all__ = ['solve01']

DIAL_NUMBERS: int = 100

def parse_step(line: str) -> tuple[bool, int]:
    direction: str = line[0]
    distance: int = int(line[1:])
    return direction == 'R', distance


def click1(position: int, zeros: int, is_right: bool, distance: int) -> tuple[int, int]:
    position += distance if is_right else -distance
    position %= DIAL_NUMBERS
    zeros += 1 if position == 0 else 0
    return position, zeros


def click2(position: int, zeros: int, is_right: bool, distance: int) -> int:
    whole_turns: int = distance // DIAL_NUMBERS
    zeros += whole_turns
    distance = distance % DIAL_NUMBERS
    if is_right:
        if position + distance >= DIAL_NUMBERS:  # passing or landing on 0 going RIGHT
            return zeros + 1
    else:
        if position != 0 and position - distance <= 0:  # passing or landing on 0 going LEFT
            return zeros + 1
    return zeros


def solve01(lines: Iterator[str]) -> Iterator[int]:

    position: int = 50

    part1: int = 0
    part2: int = 0

    for line in lines:
        is_right, distance = parse_step(line)
        part2 = click2(position, part2, is_right, distance)
        position, part1 = click1(position, part1, is_right, distance)

    yield part1
    yield part2
