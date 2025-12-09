from typing import Iterator

import numpy as np

from structures.algorithms import UnionFind


__all__ = ['solve08']


def parse_points_enumerated(lines: Iterator[str]) -> list[tuple[int, int, int]]:
    points: list[tuple[int, int, int]] = []
    for line in lines:
        x, y, z = tuple(int(token) for token in line.split(','))
        points.append((x, y, z))
    return points


def sorted_distances_squared_indexed(int_to_point: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    pairs: list[tuple[int, int, int]] = []
    for i, p1 in enumerate(int_to_point[:-1]):
        for j, p2 in enumerate(int_to_point[i + 1:], start=i+1):
            d = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
            pairs.append((d, i, j))
    pairs.sort()
    return pairs


def solve08(lines: Iterator[str]) -> Iterator[int]:

    points = parse_points_enumerated(lines)
    num_points: int = len(points)
    num_connections_required = 10 if num_points == 20 else 1000

    circuits: UnionFind = UnionFind(num_points)

    pairs: list[tuple[int, int, int]] = sorted_distances_squared_indexed(points)

    connection_attempts: int = 0
    num_connections: int = 0
    done_part: bool = False
    for _, index1, index2 in pairs:
        connection_attempts += 1
        if circuits.union(index1, index2):
            num_connections += 1
        if not done_part and connection_attempts == num_connections_required:
            sizes: list[int] = circuits.set_sizes()
            sizes.sort(reverse=True)
            part1: int = int(np.prod(sizes[:3]))
            done_part = True
            yield part1
        if len(circuits) == 1:
            part2: int = points[index1][0] * points[index2][0]
            yield part2
            return
