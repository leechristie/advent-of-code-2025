from typing import Iterator


__all__ = ['solve07']


def begin_beam(lines: Iterator[str]) -> dict[int, int]:
    first: str = next(lines)
    amplitudes: dict[int, int] = {first.index('S'): 1}
    return amplitudes


def split_beams(line: str, amplitudes: dict[int, int]) -> tuple[dict[int, int], int]:
    rv: dict[int, int] = {}
    splits: int = 0
    for i, amplitude in amplitudes.items():
        if line[i] == '^':
            rv[i - 1] = rv.get(i - 1, 0) + amplitude
            rv[i + 1] = rv.get(i + 1, 0) + amplitude
            splits += 1
        else:
            rv[i] = rv.get(i, 0) + amplitude
    return rv, splits


def solve07(lines: Iterator[str]) -> Iterator[int]:

    amplitudes = begin_beam(lines)

    num_splits: int = 0
    for line in lines:
        if '^' not in line:
            continue
        amplitudes, current_splits = split_beams(line, amplitudes)
        num_splits += current_splits

    yield num_splits

    yield sum(amplitudes.values())
