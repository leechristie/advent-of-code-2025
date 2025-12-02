from typing import Iterator, Literal, cast

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


def click2(position: int, zeros: int, is_right: bool, distance: int) -> tuple[int, int]:
    whole_turns: int = distance // DIAL_NUMBERS
    zeros += whole_turns
    distance = distance % DIAL_NUMBERS
    if is_right:
        position += distance
        if position >= DIAL_NUMBERS:  # passing or landing on 0 going RIGHT
            zeros += 1
    else:
        if position == 0:  # starting from 0 cannot roll over
            position -= distance
        else:
            position -= distance
            if position <= 0:  # passing or landing on 0 going LEFT
                zeros += 1
    position %= DIAL_NUMBERS
    return position, zeros


def solve01(lines: Iterator[str]) -> Iterator[int]:

    position: int = 50

    zeros1: int = 0
    zeros2: int = 0

    for line in lines:
        is_right, distance = parse_step(line)
        _, zeros1 = click1(position, zeros1, is_right, distance)
        position, zeros2 = click2(position, zeros2, is_right, distance)

    yield zeros1
    yield zeros2
