from typing import Iterator

from collections import defaultdict

from structures.grid import Grid
from structures.points import Point, Dimensions

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


def get_bounds(points: list[Point]) -> Dimensions:
    max_x: int = points[0].x
    max_y: int = points[0].y
    for point in points[1:]:
        if point.x > max_x:
            max_x = point.x
        if point.y > max_y:
            max_y = point.y
    width: int = max_x + 1
    height: int = max_y + 1
    return Dimensions(width=width, height=height)


def group_by_x_and_y(points: list[Point]) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    x_to_ys: dict[int, list[int]] = defaultdict(list)
    y_to_xs: dict[int, list[int]] = defaultdict(list)
    for point in points:
        x: int = point.x
        y: int = point.y
        x_to_ys[x].append(y)
        y_to_xs[y].append(x)
    return x_to_ys, y_to_xs


def create_grid(points: list[Point], padding:int = 0) -> tuple[Dimensions, Grid]:
    dimensions = get_bounds(points)
    grid: Grid = Grid.blank(dimensions, ' X-v^')
    for point in points:
        grid[point] = 'X'
    return dimensions, grid


def draw_lines(grid: Grid, points: list[Point]) -> None:

    for p1, p2 in zip(points, [points[-1]] + points[:-1]):
        grid.draw_ortholine_exclusive_no_overlap(p1, p2, '-')


def draw_vlines(grid: Grid, points: list[Point], reverse:bool = False):
    for p1, p2 in zip(points, [points[-1]] + points[:-1]):
        if p1.x == p2.x:
            if p1.y > p2.y:
                grid.draw_ortholine(p1, p2, '^' if reverse else 'v')
            else:
                grid.draw_ortholine(p1, p2, 'v' if reverse else '^')


def iter_four_corners(areas: list[tuple[int, Point, Point]]) -> Iterator[tuple[int, tuple[Point, Point], tuple[Point, Point]]]:
    for a, p1, p2 in areas:
        p3 = Point(x=p1.x, y=p2.y)
        p4 = Point(x=p2.x, y=p1.y)
        yield a, (p1, p2), (p3, p4)


def iter_four_corners_each_inside(grid: Grid, but_not_boundary_memo: Grid, areas: list[tuple[int, Point, Point]]) -> Iterator[tuple[int, tuple[Point, Point], tuple[Point, Point]]]:
    for a, (p1, p2), (p3, p4) in iter_four_corners(areas):
        if is_inside_recursive(grid, but_not_boundary_memo, p3) and is_inside_recursive(grid, but_not_boundary_memo, p4):
            yield a, (p1, p2), (p3, p4)


def __is_inside_but_not_boundary_recursive(grid: Grid, but_not_boundary_memo: Grid, point: Point) -> bool:

    if but_not_boundary_memo[point]:

        # right is off the grid, so we are outside
        if point.x + 1 >= grid.dimensions.width:
            but_not_boundary_memo[point] = 'o'
            return False

        right: Point = Point(x=point.x + 1, y=point.y)
        if grid[right] == 'v':
            but_not_boundary_memo[point] = 'i'
            return True

        if grid[right] == '^':
            but_not_boundary_memo[point] = 'o'
            return False

        if __is_inside_but_not_boundary_recursive(grid, but_not_boundary_memo, right):
            but_not_boundary_memo[point] = 'i'
            return True
        else:
            but_not_boundary_memo[point] = 'o'
            return False

    else:
        return but_not_boundary_memo[point] == 'i'


def is_inside_recursive(grid: Grid, but_not_boundary_memo: Grid, point: Point) -> bool:
    if grid[point] != ' ':
        return True
    return __is_inside_but_not_boundary_recursive(grid, but_not_boundary_memo, point)


def walk_two_points_all_inside(grid: Grid, but_not_boundary_memo: Grid, p1: Point, p2: Point) -> bool:
    if p1.x == p2.x:
        x = p1.x
        for y in range(min((p1.y, p2.y)), max((p1.y, p2.y)) + 1):
            if not is_inside_recursive(grid, but_not_boundary_memo, Point(x=x, y=y)):
                return False
    else:
        y = p1.y
        for x in range(min((p1.x, p2.x)), max((p1.x, p2.x)) + 1):
            if not is_inside_recursive(grid, but_not_boundary_memo, Point(x=x, y=y)):
                return False
    return True


def walk_points_all_inside(grid: Grid, but_not_boundary_memo: Grid, points: list[Point]) -> bool:
    for p1, p2 in zip(points, [points[-1]] + points[:-1]):
        if not walk_two_points_all_inside(grid, but_not_boundary_memo, p1, p2):
            return False
    return True


def draw_final_rect(dimensions: Dimensions, p1: Point, p2: Point) -> Grid:
    rv: Grid = Grid.blank(dimensions, '?O')
    for y in range(min((p1.y, p2.y)), max((p1.y, p2.y)) + 1):
        for x in range(min((p1.x, p2.x)), max((p1.x, p2.x)) + 1):
            p = Point(x=x, y=y)
            rv[p] = 'O'
    return rv


def get_top_left_point(points: list[Point]) -> Point:
    min_x: int = -1
    for p in points:
        if min_x == -1 or p.x < min_x:
            min_x = p.x
    min_y: int = -1
    for p in points:
        if p.x == min_x:
            if min_y == -1 or p.y < min_y:
               min_y = p.y
    return Point(x=min_x, y=min_y)


def solve_part2(points: list[Point], areas: list[tuple[int, Point, Point]]) -> tuple[int, Point, Point]:

    dimensions, grid = create_grid(points)
    draw_lines(grid, points)
    draw_vlines(grid, points)

    # reverse orientation if needed
    top_left_point: Point = get_top_left_point(points)
    top_left_point_symbol: str = grid[top_left_point]
    if top_left_point_symbol == 'v':
        draw_vlines(grid, points, reverse=True)

    but_not_boundary_memo = Grid.blank(grid.dimensions, symbols='?oi')
    for a, (p1, p2), (p3, p4) in iter_four_corners_each_inside(grid, but_not_boundary_memo, areas):
        if walk_points_all_inside(grid, but_not_boundary_memo, [p1, p3, p2, p4]):
            return a, p1, p2
    raise AssertionError('did not find solution to Part 2')


def all_areas(points: list[Point]) -> list[tuple[int, Point, Point]]:
    rv: list[tuple[int, Point, Point]] = []
    for i, p1 in enumerate(points[:-1]):
        for p2 in points[i+1:]:
            area: int = bounding_rect_area(p1, p2)
            rv.append((area, p1, p2))
    rv.sort(key=lambda x: x[0], reverse=True)
    return rv


def sorted_xs_and_ys(points: list[Point]) -> tuple[list[int], list[int]]:
    xs: set[int] = set()
    ys: set[int] = set()
    for point in points:
        xs.add(point.x)
        ys.add(point.y)
    return sorted(xs), sorted(ys)


def unsquish_point(point: Point, xs: list[int], ys:list[int]) -> Point:
    return Point(x=xs[point.x], y=ys[point.y])


def unsquish_area(rect: tuple[int, Point, Point], xs: list[int], ys:list[int]) -> tuple[int, Point, Point]:
    a, p1, p2 = rect
    p1, p2 = unsquish_point(p1, xs, ys), unsquish_point(p2, xs, ys)
    return a, p1, p2


def to_reverse_dict(values: list[int]) -> dict[int, int]:
    rv: dict[int, int] = {}
    for index, value in enumerate(values):
        rv[value] = index
    return rv


def squish_point(point: Point, xs_lookup: dict[int, int], ys_lookup: dict[int, int]) -> Point:
    return Point(x=xs_lookup[point.x], y=ys_lookup[point.y])


def squish_points(points: list[Point], xs_lookup: dict[int, int], ys_lookup: dict[int, int]) -> list[Point]:
    rv: list[Point] = []
    for point in points:
        rv.append(squish_point(point, xs_lookup, ys_lookup))
    return rv


def squish_area(area: tuple[int, Point, Point], xs_lookup: dict[int, int], ys_lookup: dict[int, int]) -> tuple[int, Point, Point]:
    a, p1, p2 = area
    p1, p2 = squish_point(p1, xs_lookup, ys_lookup), squish_point(p2, xs_lookup, ys_lookup)
    return a, p1, p2


def squish_areas(areas: list[tuple[int, Point, Point]], xs_lookup: dict[int, int], ys_lookup: dict[int, int]) -> list[tuple[int, Point, Point]]:
    rv: list[tuple[int, Point, Point]] = []
    for area in areas:
        rv.append(squish_area(area, xs_lookup, ys_lookup))
    return rv


def solve09(lines: Iterator[str]) -> Iterator[int]:

    points: list[Point] = parse_points(lines)
    areas: list[tuple[int, Point, Point]] = all_areas(points)

    part1: int = areas[0][0]
    assert 4771532800 == part1
    yield part1

    xs, ys = sorted_xs_and_ys(points)
    xs_lookup: dict[int, int] = to_reverse_dict(xs)
    ys_lookup: dict[int, int] = to_reverse_dict(ys)
    squished_points: list[Point] = squish_points(points, xs_lookup, ys_lookup)
    squished_areas = squish_areas(areas, xs_lookup, ys_lookup)
    largest_rect: tuple[int, Point, Point] = solve_part2(squished_points, squished_areas)
    part2: int = unsquish_area(largest_rect, xs, ys)[0]
    assert 1544362560 == part2
    yield part2
