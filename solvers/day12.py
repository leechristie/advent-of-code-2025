import itertools
from typing import Iterator

import numpy as np
from numpy.f2py.rules import sepdict

from printing.debug import print
from structures.grid import Grid
from structures.points import Dimensions

__all__ = ['solve12']


type Present = np.ndarray
type PresentView = np.ndarray
type Presents = list[tuple[Present, list[PresentView]]]
type Requirement = list[int]
type TreeArea = np.ndarray
type Region = tuple[TreeArea, Requirement]
type Regions = list[Region]


WIDTH: int = 3
HEIGHT: int = 3
DTYPE = np.uint8


def compute_rotations(grid: Present) -> list[PresentView]:
    rv: list[PresentView] = []
    for num_rotations in range(4):
        if num_rotations == 0:
            rv.append(grid)
        else:
            rotated: Present = grid.copy()
            rotated = np.rot90(rotated, num_rotations)
            duplicate: bool = False
            for other in rv:
                if np.array_equal(rotated, other):
                    duplicate = True
            if not duplicate:
                rv.append(rotated)
    return rv


def parse_input(lines: Iterator[str]) -> tuple[Presents, Regions]:
    presents: Presents = []
    regions: Regions = []
    for line in lines:
        if line.endswith(':'):
            grid: Grid
            grid, _ = Grid.parse(lines, symbols='.#')
            grid.cells = grid.cells.astype(dtype=DTYPE, casting='unsafe')
            assert (grid.cells.shape == (HEIGHT, WIDTH)), f'{grid.cells.shape = }'
            presents.append((grid.cells, compute_rotations(grid.cells)))
        else:
            size: str
            items: str
            size, items = line.split(': ')
            width: int
            height: int
            width, height = [int(e) for e in size.split('x')]
            requirement: Requirement = [int(e) for e in items.split(' ')]
            tree_area = np.zeros((height, width), dtype=DTYPE)
            regions.append((tree_area, requirement))
    return presents, regions


def print_array(arr: np.ndarray, indent: int = 0) -> None:
    height, width = arr.shape
    for y in range(height):
        print(' ' * indent, end='')
        for x in range(width):
            if arr[y, x] == 0:
                print('.', end='')
            else:
                print(int(arr[y, x]) % 10, end='')
        print()


def pop_present(requirement: Requirement) -> int:
    for present_id, required_count in enumerate(requirement):
        if required_count > 0:
            requirement[present_id] -= 1
            return present_id
    return -1


def push_present(presents: Requirement, present_id: int) -> None:
    presents[present_id] += 1


def fit_shapes(presents: Presents, tree_area: TreeArea, requirement: Requirement) -> bool:

    height, width = tree_area.shape

    def __fit_shapes() -> bool:

        present_id: int = pop_present(requirement)
        if present_id < 0:
            return True
        rotations: PresentView
        _, rotations = presents[present_id]

        for y, x, rotation in itertools.product(range(height - HEIGHT + 1), range(width - WIDTH + 1), rotations):
            patch = tree_area[y:y + HEIGHT, x:x + WIDTH]
            if (patch * rotation).any():
                continue
            patch = tree_area[y:y + HEIGHT, x:x + WIDTH]
            np.add(patch, rotation, patch)
            if __fit_shapes():
                return True
            np.subtract(patch, rotation, patch)

        push_present(requirement, present_id)
        return False

    return __fit_shapes()


def solve12(lines: Iterator[str]) -> Iterator[int]:

    presents: Presents
    regions: Regions
    presents, regions = parse_input(lines)

    part1: int = 0
    for index, region in enumerate(regions):
        tree_area, requirement = region
        print(f'solving line {index}. . . ', end='')
        if fit_shapes(presents, tree_area, requirement):
            print('SOLVED')
            part1 += 1
        else:
            print('NO SOLUTION')

    yield part1
