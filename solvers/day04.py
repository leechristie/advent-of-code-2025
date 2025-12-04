from typing import Iterator
from printing.debug import print

__all__ = ['solve04']

from structures.grid import Grid


def elf_trip(grid: Grid) -> int:
    num_removed: int = 0
    for point in grid.positions():
        if grid[point] == '@':
            num_neighbour_rolls = 0
            for neighbour in grid.neighbours(point):
                if grid[neighbour] == '@' or grid[neighbour] == 'x':
                    num_neighbour_rolls += 1
            if num_neighbour_rolls < 4:
                grid[point] = 'x'
                num_removed += 1
    return num_removed


def solve04(lines: Iterator[str]) -> Iterator[int]:

    grid: Grid
    grid, _ = Grid.parse(lines, '.@x')

    num_removed: int
    num_removed = elf_trip(grid)
    part1: int = num_removed
    part2: int = num_removed

    while num_removed:
        grid.replace('x', '.')
        num_removed = elf_trip(grid)
        part2 += num_removed

    yield part1
    yield part2
