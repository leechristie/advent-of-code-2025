import time
from typing import Iterator

from collections import defaultdict

import tqdm

from printing.color import ASCII_CYAN, color_print
from printing.debug import print

from structures.grid import Grid
from structures.points import Point, Dimensions, Velocity

__all__ = ['solve09']


def parse_points(lines: Iterator[str]) -> list[Point]:
    rv: list[Point] = []
    for line in lines:
        x, y = line.split(',')
        rv.append(Point(x=int(x), y=int(y)))
    return rv


def bounding_rect_area(p1: Point, p2: Point) -> int:
    dx: int = abs(p1.x - p2.x) + 1
    dy: int = abs(p1.y - p2.y) + 1
    return dx * dy


def get_bounds(points: list[Point], *, padding: int = 0) -> tuple[Velocity, Dimensions]:
    assert points
    min_x: int = points[0].x
    min_y: int = points[0].y
    max_x: int = points[0].x
    max_y: int = points[0].y
    for point in points[1:]:
        if point.x < min_x:
            min_x = point.x
        if point.x > max_x:
            max_x = point.x
        if point.y < min_y:
            min_y = point.y
        if point.y > max_y:
            max_y = point.y
    min_x -= padding
    min_y -= padding
    max_x += padding
    max_y += padding
    width: int = max_x - min_x + 1
    height: int = max_y - min_y + 1
    return Velocity(dx=min_x, dy=min_y), Dimensions(width=width, height=height)


def group_by_x_and_y(points: list[Point]) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    x_to_ys: dict[int, list[int]] = defaultdict(list)
    y_to_xs: dict[int, list[int]] = defaultdict(list)
    for point in points:
        x: int = point.x
        y: int = point.y
        x_to_ys[x].append(y)
        y_to_xs[y].append(x)
    return x_to_ys, y_to_xs


def create_grid(points: list[Point]) -> tuple[Velocity, Dimensions, Grid]:
    offset, dimensions = get_bounds(points, padding=1)
    grid: Grid = Grid.blank(dimensions, '.X# iv^')
    for point in points:
        grid[point - offset] = 'X'
    return offset, dimensions, grid


def draw_lines(grid: Grid, offset: Velocity, points: list[Point]) -> None:
    for p1, p2 in zip(points, [points[-1]] + points[:-1]):
        grid.draw_ortholine(p1 - offset, p2 - offset, '#')
    for p1, p2 in zip(points, [points[-1]] + points[:-1]):
        if p1.x == p2.x:
            if p1.y > p2.y:
                grid.draw_ortholine(p1 - offset, p2 - offset, '^')
            else:
                grid.draw_ortholine(p1 - offset, p2 - offset, 'v')


def flood_fill(grid: Grid) -> None:
    grid.flood_fill(Point(x=0, y=0), ' ')


def debug_print_example_grid(grid: Grid) -> None:
    if grid.dimensions.height < 100:
        print(grid, end='\n\n')


__start: float = 0
def timer(message: str | None = None):
    global __start
    now: float = time.perf_counter()
    if __start != 0:
        if message:
            color_print(message, ':', f'{(now - __start) * 1000:.2f} ms', color=ASCII_CYAN)
    __start = now


def iter_four_corners(areas: list[tuple[int, Point, Point]]) -> Iterator[tuple[int, tuple[Point, Point], tuple[Point, Point]]]:
    for a, p1, p2 in areas:
        p3 = Point(x=p1.x, y=p2.y)
        p4 = Point(x=p2.x, y=p1.y)
        yield a, (p1, p2), (p3, p4)


def is_inside(grid: Grid, point: Point) -> bool:
    if grid[point] == '#' or grid[point] == '^' or grid[point] == 'v':
        return True
    step: Velocity = Velocity(dx=1, dy=0)
    # point += step
    blocks: list[str] = []
    block: str = ''
    while point in grid.dimensions:

        if grid[point] == '^':
            if block:
                block += '^'
                blocks.append(block)
                block = ''
            else:
                block = '^'

        elif grid[point] == 'v':
            if block:
                block += 'v'
                blocks.append(block)
                block = ''
            else:
                block = 'v'

        elif grid[point] == '#':
            assert block, point
            if block.endswith('v') or block.endswith('^'):
                block += '#'

        else:
            if block:
                blocks.append(block)
                block = ''

        point += step
    assert (not block), point
    inside: bool = False
    for block in blocks:
        if len(block) == 1:
            inside = not inside
        else:
            first, last = block[0], block[-1]
            if first == last:
                inside = not inside
    return inside


def solve_part2(points: list[Point], areas: list[tuple[int, Point, Point]]) -> int:

    timer()
    offset, dimensions, grid = create_grid(points)
    timer('created grid of red tiles')
    debug_print_example_grid(grid)
    timer()

    draw_lines(grid, offset, points)
    timer('drawn lines of green tiles')
    debug_print_example_grid(grid)
    timer()

    if grid.dimensions.height < 100:
        copy: Grid = grid.copy()
        for y in range(dimensions.height):
            for x in range(dimensions.width):
                p: Point = Point(x=x, y=y)
                if is_inside(grid, p):
                    copy[p] = 'i'
        timer('debug filling inside')
        debug_print_example_grid(copy)
        timer()

    for a, (p1, p2), (p3, p4) in tqdm.tqdm(list(iter_four_corners(areas))):
        assert is_inside(grid, p1 - offset)
        assert is_inside(grid, p1 - offset)
        if is_inside(grid, p3 - offset) and is_inside(grid, p4 - offset):
            timer('looped over all sets of potential 4 corners')
            return a
    raise ValueError('ran out of sets of 4 corners to check')



def all_areas(points: list[Point]) -> list[tuple[int, Point, Point]]:
    rv: list[tuple[int, Point, Point]] = []
    for i, p1 in enumerate(points[:-1]):
        for p2 in points[i+1:]:
            area: int = bounding_rect_area(p1, p2)
            rv.append((area, p1, p2))
    rv.sort(key=lambda x: x[0], reverse=True)
    return rv


def solve09(lines: Iterator[str]) -> Iterator[int]:

    points: list[Point] = parse_points(lines)
    areas: list[tuple[int, Point, Point]] = all_areas(points)

    part1: int = areas[0][0]
    assert (part1 in (50, 4771532800)), f'part1 = {part1}'
    yield part1

    part2: int = solve_part2(points, areas)
    yield part2
