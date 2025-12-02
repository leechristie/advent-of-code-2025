from typing import Iterator, Literal, cast

__all__ = ['solve01']

DIAL_NUMBERS: int = 100

def parse_step(line: str) -> tuple[Literal['L', 'R'], int]:
    direction: str = line[0]
    distance: int = int(line[1:])
    direction_literal = cast(Literal['L', 'R'], direction)
    return direction_literal, distance


def click1(position: int, zeros: int, direction: Literal['L', 'R'], distance: int) -> tuple[int, int]:
    position += distance if direction == 'R' else -distance
    position %= DIAL_NUMBERS
    zeros += 1 if position == 0 else 0
    return position, zeros


def click2(position: int, zeros: int, direction: Literal['L', 'R'], distance: int) -> tuple[int, int]:
    whole_turns: int = distance // DIAL_NUMBERS
    zeros += whole_turns
    distance = distance % DIAL_NUMBERS
    if direction == 'R':
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
        direction, distance = parse_step(line)
        _, zeros1 = click1(position, zeros1, direction, distance)
        position, zeros2 = click2(position, zeros2, direction, distance)

    yield zeros1
    yield zeros2
