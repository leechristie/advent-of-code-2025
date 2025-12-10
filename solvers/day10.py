import itertools
import time
from collections.abc import Callable
from typing import Iterator
from structures.astar import a_star

from printing.color import ASCII_PURPLE, color_print
from printing.debug import print

__all__ = ['solve10']


def parse_machine(line: str) -> tuple[list[bool], list[tuple[int, ...]], list[int]]:
    required_lights: list[bool]
    buttons: list[tuple[int, ...]] = []
    required_joltages: list[int]
    tokens: list[str] = line.split(' ')
    light_str, button_tokens, joltage_str = tokens[0], tokens[1:-1], tokens[-1]
    light_str = light_str.removeprefix('[').removesuffix(']')
    joltage_str = joltage_str.removeprefix('{').removesuffix('}')
    required_lights = [True if e == '#' else False for e in light_str]
    for button_token in button_tokens:
        button_token = button_token.removeprefix('(').removesuffix(')')
        buttons.append(tuple([int(e) for e in button_token.split(',')]))
    required_joltages = [int(e) for e in joltage_str.split(',')]
    return required_lights, buttons, required_joltages


def parse_machines(lines: Iterator[str]) -> Iterator[tuple[list[bool], list[tuple[int, ...]], list[int]]]:
    for line in lines:
        yield parse_machine(line)


def button_press_result(num_lights: int, buttons_presses: tuple[tuple[int, ...], ...]) -> list[bool]:
    rv: list[bool] = [False] * num_lights
    for button in buttons_presses:
        for light_index in button:
            rv[light_index] = not rv[light_index]
    return rv


def is_correct_press_combination(required_lights: list[bool], buttons_presses: tuple[tuple[int, ...], ...]):
    result: list[bool] = button_press_result(len(required_lights), buttons_presses)
    return required_lights == result


def fewest_presses(required_lights: list[bool], buttons: list[tuple[int, ...]]) -> int:
    for presses in itertools.count(0):
        for combination in itertools.combinations(buttons, presses):
            if is_correct_press_combination(required_lights, combination):
                return presses
    raise AssertionError


def can_press(goal: list[int] | tuple[int, ...], button: tuple[int, ...]) -> bool:
    for i in button:
        if goal[i] == 0:
            return False
    return True


def press_button(goal: list[int], button: tuple[int, ...]) -> None:
    for i in button:
        goal[i] -= 1


def unpress_button(goal: list[int], button: tuple[int, ...]) -> None:
    for i in button:
        goal[i] += 1


def with_button_pressed(goal: list[int] | tuple[int, ...], button: tuple[int, ...]) -> tuple[int, ...]:
    rv: list[int] = list(goal)
    for i in button:
        rv[i] -= 1
    return tuple(rv)


NO_SOLUTION: int = -1


def fewest_presses_for_joltage_memoized(required_joltages: list[int], buttons: list[tuple[int, ...]]) -> int:
    memo: dict[tuple[int, ...], int] = {}
    def __fewest_presses_for_joltage() -> int | None:
        t: tuple[int, ...] = tuple(required_joltages)
        if t in memo:
            return memo[t]
        if sum(required_joltages) == 0:
            memo[t] = 0
            return 0
        lowest_remaining: int = NO_SOLUTION
        for button in buttons:
            if can_press(required_joltages, button):
                press_button(required_joltages, button)
                if sum(required_joltages) == 0:
                    unpress_button(required_joltages, button)
                    memo[t] = 1
                    return 1
                remaining_presses: int = __fewest_presses_for_joltage()
                if remaining_presses != NO_SOLUTION:
                    if lowest_remaining == NO_SOLUTION or remaining_presses < lowest_remaining:
                        lowest_remaining = remaining_presses
                unpress_button(required_joltages, button)
        if lowest_remaining != NO_SOLUTION:
            lowest_remaining += 1
        memo[t] = lowest_remaining
        return lowest_remaining
    return __fewest_presses_for_joltage()


def fewest_presses_for_joltage_by_a_star(required_joltages: list[int], buttons: list[tuple[int, ...]]) -> int:

    start: tuple[int, ...] = tuple(required_joltages)
    goal: Callable[[tuple[int, ...]], bool] = lambda x: sum(x) == 0
    heuristic: Callable[[tuple[int, ...]], int] = max
    def neighbours(joltages: tuple[int, ...]) -> list[tuple[tuple[int, ...], int]]:
        rv: list[tuple[tuple[int, ...], int]] = []
        for button in buttons:
            if can_press(joltages, button):
                rv.append((with_button_pressed(joltages, button), 1))
        return rv
    result: list[tuple[int, ...]] | None = a_star(start, goal, heuristic, neighbours)
    return len(result) - 1


def possible_ranges(required_joltages: list[int], buttons: list[tuple[int, ...]]) -> list[tuple[int, int]]:
    rv: list[list[int]] = [[0, max(required_joltages)] for _ in range(len(buttons))]
    for index, required_joltage in enumerate(required_joltages):
        supported_button_ids: list[int] = []
        for button_id, button in enumerate(buttons):
            if index in button:
                supported_button_ids.append(button_id)
        assert len(supported_button_ids) > 0
        if len(supported_button_ids) == 1:
            button_id: int = supported_button_ids[0]
            press_count: int = required_joltage
            assert rv[button_id][0] <= press_count
            assert rv[button_id][1] >= press_count
            rv[button_id][0] = press_count
            rv[button_id][1] = press_count
        else:
            max_press_count: int = required_joltage
            for button_id in supported_button_ids:
                if rv[button_id][1] > max_press_count:
                    rv[button_id][1] = max_press_count
                    assert rv[button_id][0] <= rv[button_id][1]

    return [(minimum, maximum) for minimum, maximum in rv]

        
def solve10(lines: Iterator[str]) -> Iterator[int]:

    part1: int = 0
    part2: int = 0

    machines: list[tuple[list[bool], list[tuple[int, ...]], list[int]]] = list(parse_machines(lines))

    for required_lights, buttons, required_joltages in machines:
        part1 += fewest_presses(required_lights, buttons)

    assert (part1 in (7, 494)), f'part1 = {part1}'
    yield part1
    
    for i, (required_lights, buttons, required_joltages) in enumerate(machines, start=1):
        print(f'solving machine {i} of {len(machines)} . . .')
        print('   ', required_lights)
        print('   ', buttons)
        print('   ', required_joltages)
        print('    start :', time.strftime('%X %x %Z'))
        start: float = time.perf_counter()
        #current: int = fewest_presses_for_joltage_memoized(required_joltages, buttons)
        for button, (minimum, maximum) in zip(buttons, possible_ranges(required_joltages, buttons)):
            print(f'        button {button} to be pressed {minimum} to {maximum} times')
        current: int = fewest_presses_for_joltage_by_a_star(required_joltages, buttons)
        taken: float = time.perf_counter() - start
        print(f'    took : {taken / 60:.1f} minutes')
        print(f'    answer: {current}')
        print()
        part2 += current

    if 7 == part1:
        assert 33 == part2
    yield part2
