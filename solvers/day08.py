import math
import random
import time
from typing import Iterator

import numpy as np

from printing.color import ASCII_RED, color_print
from printing.debug import print
from structures.algorithms import *

from structures.points import Point3D


__all__ = ['solve08']


def parse_points_enumerated(lines: Iterator[str]) -> list[Point3D]:
    points: list[Point3D] = []
    for line in lines:
        x, y, z = [int(token) for token in line.split(',')]
        points.append(Point3D(x=x, y=y, z=z))
    return points


def sorted_distances_squared_indexed(int_to_point: list[Point3D]) -> list[tuple[int, int, int]]:
    pairs: list[tuple[int, int, int]] = []
    for i, p1 in enumerate(int_to_point[:-1]):
        for j, p2 in enumerate(int_to_point[i + 1:], start=i+1):
            d = p1.squared_euclidean(p2)
            pairs.append((d, i, j))
    pairs.sort()
    return pairs


__start: float = 0
def timer(message: str | None = None):
    global __start
    now: float = time.perf_counter()
    if __start != 0:
        if message:
            print(message, ':', f'{(now - __start) * 1000:.1f} ms')
        else:
            print(f'{(now - __start) * 1000:.1f} ms')
    __start = now


def solve08(lines: Iterator[str]) -> Iterator[int]:

    #timer()

    points = parse_points_enumerated(lines)
    num_points: int = len(points)
    num_connections_required = 10 if num_points == 20 else 1000

    #timer('load points')

    circuits: IntUnionFind = IntUnionFind(num_points)

    #timer('create union find')

    pairs: list[tuple[int, int, int]] = sorted_distances_squared_indexed(points)

    #timer('sort distances')

    connection_attempts: int = 0
    num_connections: int = 0
    part1 = None
    part2 = None
    for _, index1, index2 in pairs:
        connection_attempts += 1
        if circuits.union(index1, index2):
            num_connections += 1
        if part1 is None and connection_attempts == num_connections_required:
            part1 = int(np.prod(sorted([len(s) for s in circuits.to_sets()], reverse=True)[:3]))
            #timer('mst up to required connections')
            yield part1
        if len(circuits) == 1:
            part2 = points[index1].x * points[index2].x
            break

    #timer('remainder of mst')

    assert part1 is not None

    yield part2

    #assert (part1, part2) in ((40, 25272), (75680, 8995844880))
