from collections import defaultdict
from typing import Iterator, cast


__all__ = ['solve05']


type FreshRange = tuple[int, int]


def parse_fresh_ranges(lines: Iterator[str]) -> list[FreshRange]:
    rv: list[FreshRange] = []
    for line in lines:
        if not line:
            return rv
        lower, upper = line.split('-')
        rv.append((int(lower), int(upper) + 1))  # converts upper to bound
    raise AssertionError('bad input file')


def parse_ingredients(lines: Iterator[str]) -> Iterator[int]:
    for line in lines:
        yield int(line)


def if_in_fresh_range(ingredient: int, fresh_range: FreshRange) -> bool:
    lower, bound = fresh_range
    return lower <= ingredient < bound


def is_fresh(ingredient: int, fresh_ranges: list[FreshRange]) -> bool:
    for fresh_range in fresh_ranges:
        if if_in_fresh_range(ingredient, fresh_range):
            return True
    return False


def number_of_fresh_ingredients(lines: Iterator[str], fresh_ranges: list[FreshRange]) -> int:
    fresh_count: int = 0
    for ingredient in parse_ingredients(lines):
        if is_fresh(ingredient, fresh_ranges):
            fresh_count += 1
    return fresh_count


def eliminate_by_same_lower(fresh_ranges: list[FreshRange]) -> list[FreshRange]:
    lower_to_bounds: dict[int, list[int]] = defaultdict(list)
    for fresh_range in fresh_ranges:
        lower, bound = fresh_range
        lower_to_bounds[lower].append(bound)
    new_fresh_ranges: list[FreshRange] = []
    for lower, bounds in lower_to_bounds.items():
        new_fresh_ranges.append((lower, max(bounds)))
    return new_fresh_ranges


def eliminate_by_same_bound(fresh_ranges: list[FreshRange]) -> list[FreshRange]:
    bound_to_lowers: dict[int, list[int]] = defaultdict(list)
    for fresh_range in fresh_ranges:
        lower, bound = fresh_range
        bound_to_lowers[bound].append(lower)
    new_fresh_ranges: list[FreshRange] = []
    for bound, lowers in bound_to_lowers.items():
        new_fresh_ranges.append((min(lowers), bound))
    return new_fresh_ranges


def eliminate_by_same_lower_or_same_bound(fresh_ranges: list[FreshRange]) -> list[FreshRange]:
    fresh_ranges = eliminate_by_same_lower(fresh_ranges)
    return eliminate_by_same_bound(fresh_ranges)


def join_adjacent(fresh_ranges: list[FreshRange]) -> list[FreshRange]:

    bound_to_lower: dict[int, int] = {}
    for fresh_range in fresh_ranges:
        lower, bound = fresh_range
        bound_to_lower[bound] = lower

    keep_joining: bool = True
    while keep_joining:
        for bound, lower in bound_to_lower.items():

            if lower in bound_to_lower:
                other_lower, other_bound = bound_to_lower[lower], lower

            ## rem: supposed to be optimisation, but goes slower
            # elif lower + 1 in bound_to_lower:
            #     other_lower, other_bound = bound_to_lower[lower + 1], lower + 1

            else:
                continue

            del bound_to_lower[other_bound]
            bound_to_lower[bound] = other_lower
            keep_joining = True
            break

        else:
            keep_joining = False

    fresh_ranges = []
    for bound, lower in bound_to_lower.items():
        fresh_ranges.append((lower, bound))
    return fresh_ranges


def generate_sorted_points(fresh_ranges: list[FreshRange]) -> list[tuple[int, FreshRange]]:
    rv: list[tuple[int, FreshRange]] = []
    for lower, bound in fresh_ranges:
        rv.append((lower, (lower, bound)))
        rv.append((bound, (lower, bound)))
    rv.sort()
    return rv


def to_sorted_non_overlapping_ranges(fresh_ranges: list[FreshRange]) -> list[FreshRange]:
    sorted_points: list[tuple[int, FreshRange]] = generate_sorted_points(fresh_ranges)
    active_ranges: set[FreshRange] = set()
    previous_point: int | None = None
    rv: list[FreshRange] = []
    for point, current_range in sorted_points:
        if active_ranges:
            rv.append((cast(int, previous_point), point))
        lower, bound = current_range
        if point == lower:
            active_ranges.add(current_range)
        else:
            active_ranges.remove(current_range)
        previous_point = point
    return rv


def sum_sorted_non_overlapping_ranges(fresh_ranges: list[FreshRange]) -> int:
    rv: int = 0
    for lower, bound in fresh_ranges:
        rv += bound - lower
    return rv


def solve05(lines: Iterator[str]) -> Iterator[int]:

    fresh_ranges: list[FreshRange] = parse_fresh_ranges(lines)
    fresh_ranges = eliminate_by_same_lower_or_same_bound(fresh_ranges)
    fresh_ranges = join_adjacent(fresh_ranges)
    fresh_ranges = to_sorted_non_overlapping_ranges(fresh_ranges)
    fresh_ranges = join_adjacent(fresh_ranges)

    yield number_of_fresh_ingredients(lines, fresh_ranges)
    yield sum_sorted_non_overlapping_ranges(fresh_ranges)
