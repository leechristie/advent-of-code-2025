from typing import Iterator
from printing.debug import print

from structures.points import Point3D


__all__ = ['solve08']


def parse_points(lines: Iterator[str]) -> list[Point3D]:
    rv: list[Point3D] = []
    for line in lines:
        x, y, z = [int(token) for token in line.split(',')]
        rv.append(Point3D(x=x, y=y, z=z))
    return rv


def solve08(lines: Iterator[str]) -> Iterator[int]:

    points: list[Point3D] = parse_points(lines)

    for point in points:
        print(point)

    yield 0
    yield 0
