import itertools
import time
from collections.abc import Callable
from typing import Iterator, cast
from structures.astar import a_star

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


def can_press(goal: list[int] | tuple[int, ...], button: None | tuple[int, ...]) -> bool:
    if button is None:
        return False
    for i in button:
        if goal[i] == 0:
            return False
    return True


def press_button(goal: list[int], button: tuple[int, ...], times: int = 1) -> None:
    for i in button:
        # assert goal[i] - times >= 0  # remove
        goal[i] -= times


def unpress_button(goal: list[int], button: tuple[int, ...]) -> None:
    for i in button:
        goal[i] += 1


def with_button_pressed(goal: list[int] | tuple[int, ...], button: tuple[int, ...]) -> tuple[int, ...]:
    rv: list[int] = list(goal)
    for i in button:
        rv[i] -= 1
    return tuple(rv)


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
    assert (result is not None), 'A Star search returned None'
    return len(cast(list[tuple[int, ...]], result)) - 1


def possible_ranges(required_joltages: list[int], buttons: list[tuple[int, ...]]) -> tuple[list[int], list[int], list[int], list[set[int]]]:
    affecting_button_counts: list[int] = [0] * len(required_joltages)
    mimimums: list[int] = [0] * len(buttons)
    maximums: list[int] = [max(required_joltages)] * len(buttons)
    friends: list[set[int]] = [set() for _ in range(len(buttons))]
    for index, required_joltage in enumerate(required_joltages):
        supported_button_ids: list[int] = []
        for button_id, button in enumerate(buttons):
            if button is not None:
                if index in button:
                    supported_button_ids.append(button_id)
            else:
                mimimums[button_id] = 0
                maximums[button_id] = 0
        assert len(supported_button_ids) > 0
        if len(supported_button_ids) == 1:
            button_id_to_delete: int = supported_button_ids[0]
            press_count: int = required_joltage
            assert mimimums[button_id_to_delete] <= press_count
            assert maximums[button_id_to_delete] >= press_count
            mimimums[button_id_to_delete] = press_count
            maximums[button_id_to_delete] = press_count
        else:
            max_press_count: int = required_joltage
            for button_id in supported_button_ids:
                friends[button_id].update(set(supported_button_ids) - {button_id})
                if maximums[button_id] > max_press_count:
                    maximums[button_id] = max_press_count
                    assert (mimimums[button_id] <= maximums[button_id]), f'mimimums[{button_id}] = {mimimums[button_id]}, maximums[{button_id}] = {maximums[button_id]}'
        affecting_button_counts[index] = len(supported_button_ids)
    return affecting_button_counts, mimimums, maximums, friends


def debug_print(goal, affecting_button_counts, buttons, minimums, maximums, friends):
    print(f'    goal = {goal}')
    print(f'    affect = {affecting_button_counts}')
    for button_id, (minimum, maximum, friend_buttons) in enumerate(zip(minimums, maximums, friends)):
        if buttons[button_id] is not None:
            print(f'    #{button_id} {buttons[button_id]} to be {minimum} to {maximum} times, affects {friend_buttons}')
        else:
            print(f'    #{button_id} is dead')


def __discount_influence(affecting_button_counts,
                         button):
    for index in button:
        affecting_button_counts[index] -= 1


def __disassociate_from_friends(goal, buttons, maximums, friends,
                                button_id):
    for friend_id in friends[button_id]:
        friends[friend_id].remove(button_id)
        for index in buttons[friend_id]:
            if goal[index] < maximums[friend_id]:
                maximums[friend_id] = goal[index]


def __force_move_press_and_delete_button(goal, affecting_button_counts, buttons, maximums, friends, button_id, button, times) -> int:
    print(f'  pressing and deleting button #{button_id} {buttons[button_id]} {times} times . . .')
    rv = times
    press_button(goal, button, times)
    __discount_influence(affecting_button_counts, button)
    __disassociate_from_friends(goal, buttons, maximums, friends, button_id)
    buttons[button_id] = None
    return rv


def __forced_move_just_delete_button(goal, affecting_button_counts, buttons, minimums, maximums, friends, button_id, button) -> None:
    print(f'  deleting button #{button_id} {buttons[button_id]} with no further pressed . . .')
    __discount_influence(affecting_button_counts, button)
    __disassociate_from_friends(goal, buttons, maximums, friends, button_id)
    buttons[button_id] = None


def __single_affecting_button(buttons, index):
    for button_id, button in enumerate(buttons):
        if button is not None and index in button:
            return button_id
    raise AssertionError


def apply_forced_moves(goal, affecting_button_counts, buttons, minimums, maximums, friends) -> int:
    rv: int = 0
    print('  applying forced moves . . .')
    continue_looking: bool = True
    while continue_looking:
        continue_looking = False
        for button_id, button in enumerate(buttons):
            if button is not None:
                if minimums[button_id] == maximums[button_id]:
                    times: int = minimums[button_id]
                    if times > 0:
                        rv += __force_move_press_and_delete_button(goal, affecting_button_counts, buttons, maximums, friends, button_id, button, times)
                    else:
                        __forced_move_just_delete_button(goal, affecting_button_counts, buttons, minimums, maximums, friends, button_id, button)
                    continue_looking = True
                    break
        if continue_looking:
            debug_print(goal, affecting_button_counts, buttons, minimums, maximums, friends)
            continue
        for index, (remain, affect) in enumerate(zip(goal, affecting_button_counts)):
            if affect == 1:
                button_id = __single_affecting_button(buttons, index)
                button = buttons[button_id]
                times = maximums[button_id]
                rv += __force_move_press_and_delete_button(goal, affecting_button_counts, buttons, maximums, friends, button_id, button, times)
                continue_looking = True
                break
        if continue_looking:
            debug_print(goal, affecting_button_counts, buttons, minimums, maximums, friends)
    print('  no more forced moves.')
    return rv


def setup_step(goal, buttons):
    rv: int = 0
    affecting_button_counts, minimums, maximums, friends = possible_ranges(goal, buttons)
    print('  starting state for new solution:')
    debug_print(goal, affecting_button_counts, buttons, minimums, maximums, friends)
    rv += apply_forced_moves(goal, affecting_button_counts, buttons, minimums, maximums, friends)
    return rv, affecting_button_counts, minimums, maximums, friends


def remove_dead_buttons(buttons, maximums) -> tuple[list[tuple[int, ...]], list[int]]:
    rv_buttons: list[tuple[int, ...]] = []
    rv_maximums: list[int] = []
    for b, m in zip(buttons, maximums):
        if b is not None:
            rv_buttons.append(b)
            rv_maximums.append(m)
    return rv_buttons, rv_maximums


def fewest_presses_for_joltage_by_pruning(goal: list[int], buttons: list[tuple[int, ...]], maximums: list[int]) -> int:
    print(f'  {goal = }')
    print(f'  {buttons = }')
    print(f'  {maximums = }')
    return 0  # TODO


def solve10(lines: Iterator[str]) -> Iterator[int]:

    machines: list[tuple[list[bool], list[tuple[int, ...]], list[int]]] = list(parse_machines(lines))

    part1: int = 0
    for required_lights, buttons, required_joltages in machines:
        part1 += fewest_presses(required_lights, buttons)
    assert (part1 in (7, 494)), f'part1 = {part1}'
    yield part1

    part2: int = 0
    for i, (required_lights, buttons, required_joltages) in enumerate(machines, start=1):
        print(f'solving machine {i} of {len(machines)} . . .')
        print(' ', required_lights)
        print(' ', buttons)
        print(' ', required_joltages)
        print('  start :', time.strftime('%X %x %Z'))
        start: float = time.perf_counter()
        setup_moves, _, _, maximums, _ = setup_step(required_joltages, buttons)
        current: int = setup_moves
        buttons, maximums = remove_dead_buttons(buttons, maximums)
        current += fewest_presses_for_joltage_by_pruning(required_joltages, buttons, maximums)
        current += fewest_presses_for_joltage_by_a_star(required_joltages, buttons)
        taken: float = time.perf_counter() - start
        print(f'  took : {taken / 60:.1f} minutes')
        print(f'  answer: {current}')
        print()
        part2 += current

    if 7 == part1:
        assert 33 == part2
    yield part2
