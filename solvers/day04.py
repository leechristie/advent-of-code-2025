from typing import Iterator

__all__ = ['solve04']

from structures.grid import Grid


def elf_trip(grid: Grid) -> int:
    num_removed: int = 0
    for point in grid.positions():
        if grid[point] == '@':
            if grid.count_non_zero_neighbours(point) < 4:
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
