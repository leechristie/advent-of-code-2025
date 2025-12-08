import math
import random
from typing import Iterator

import numpy as np

from printing.color import ASCII_RED, color_print
from printing.debug import print
from structures.algorithms import *

from structures.points import Point3D


__all__ = ['solve08']


def parse_points(lines: Iterator[str]) -> list[Point3D]:
    rv: list[Point3D] = []
    for line in lines:
        x, y, z = [int(token) for token in line.split(',')]
        rv.append(Point3D(x=x, y=y, z=z))
    return rv


def sorted_distances_squared(points: list[Point3D]) -> list[tuple[int, Point3D, Point3D]]:
    pairs: list[tuple[int, Point3D, Point3D]] = []
    for i, p1 in enumerate(points[:-1]):
        for p2 in points[i + 1:]:
            d = p1.squared_euclidean(p2)
            pairs.append((d, p1, p2))
    pairs.sort()
    return pairs


def solve08(lines: Iterator[str]) -> Iterator[int]:

    points: list[Point3D] = parse_points(lines)
    circuits: UnionFind[Point3D] = UnionFind(points)

    num_connections_required = 10 if len(points) == 20 else 1000

    pairs: list[tuple[int, Point3D, Point3D]] = sorted_distances_squared(points)

    connection_attempts: int = 0
    num_connections: int = 0
    part1 = None
    part2 = None
    for _, p1, p2 in pairs:
        connection_attempts += 1
        if circuits.union(p1, p2):
            num_connections += 1
        if part1 is None and connection_attempts == num_connections_required:
            part1 = int(np.prod(sorted([len(s) for s in circuits.to_sets()], reverse=True)[:3]))
            yield part1
        if len(circuits) == 1:
            part2 = p1.x * p2.x
            break

    assert part1 is not None

    yield part2

    assert 75680 == part1
    assert 8995844880 == part2
