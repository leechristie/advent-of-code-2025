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
type Requirement = dict[int, int]
type TreeArea = np.ndarray
type Regions = list[tuple[TreeArea, Requirement]]


WIDTH: int = 3
HEIGHT: int = 3


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
            grid.cells = grid.cells.astype(dtype=np.bool, casting='unsafe')
            assert (grid.cells.shape == (HEIGHT, WIDTH)), f'{grid.cells.shape = }'
            presents.append((grid.cells, compute_rotations(grid.cells)))
        else:
            required_presents: Requirement = {}
            size: str
            items: str
            size, items = line.split(': ')
            width: int
            height: int
            width, height = [int(e) for e in size.split('x')]
            for index, number in enumerate([int(e) for e in items.split(' ')]):
                if number:
                    required_presents[index] = number
            tree_area = np.zeros((height, width), dtype=np.bool)
            regions.append((tree_area, required_presents))
    return presents, regions


def print_array(arr: np.ndarray, indent: int = 0) -> None:
    height, width = arr.shape
    for y in range(height):
        print(' ' * indent, end='')
        for x in range(width):
            print('X' if arr[y, x] else '.', end='')
        print()


def solve12(lines: Iterator[str]) -> Iterator[int]:

    presents: Presents
    regions: Regions
    presents, regions = parse_input(lines)

    for index, (present, rotations) in enumerate(presents):
        print(f'{index}:')
        print_array(present)
        print()

    for tree_area, required in regions:
        print_array(tree_area)
        print(required)
        print()

    yield 0
