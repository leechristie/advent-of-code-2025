from typing import Iterator

from structures.grid import Grid
from structures.points import Point


__all__ = ['solve04']


def elf_trip(grid: Grid) -> int:
    num_removed: int = 0
    for point in grid.positions():
        if grid[point] == '@':
            if grid.count_non_zero_neighbours(point) < 4:
                grid[point] = 'x'
                num_removed += 1
    return num_removed


# version only exists for speed optimisation - can use elf_trip for same answer
def sparse_elf_trip(grid: Grid, roll_locations: list[Point]) -> tuple[int, list[Point]]:
    num_removed: int = 0
    new_roll_locations: list[Point] = []
    removed_roll_locations: list[Point] = []
    for point in roll_locations:
        if grid.count_neighbours(point, '@') < 4:
            num_removed += 1
            removed_roll_locations.append(point)
        else:
            new_roll_locations.append(point)
    grid.set_all(removed_roll_locations, '.')
    return num_removed, new_roll_locations


def solve04(lines: Iterator[str]) -> Iterator[int]:

    grid: Grid
    grid, _ = Grid.parse(lines, '.@x')

    num_removed = elf_trip(grid)
    yield num_removed

    grid.replace('x', '.')
    roll_locations: list[Point] = grid.locations_of('@')
    total_removed: int = num_removed
    while num_removed:
        num_removed, roll_locations = sparse_elf_trip(grid, roll_locations)
        total_removed += num_removed
    yield total_removed
