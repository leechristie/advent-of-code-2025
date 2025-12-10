import itertools
from typing import Iterator


__all__ = ['solve10']


def parse_machine(line: str) -> tuple[list[bool], list[set[int]], list[int]]:
    required_lights: list[bool]
    buttons: list[set[int]] = []
    required_joltage: list[int]
    tokens: list[str] = line.split(' ')
    light_str, button_tokens, joltage_str = tokens[0], tokens[1:-1], tokens[-1]
    light_str = light_str.removeprefix('[').removesuffix(']')
    joltage_str = joltage_str.removeprefix('{').removesuffix('}')
    required_lights = [True if e == '#' else False for e in light_str]
    for button_token in button_tokens:
        button_token = button_token.removeprefix('(').removesuffix(')')
        buttons.append({int(e) for e in button_token.split(',')})
    required_joltage = [int(e) for e in joltage_str.split(',')]
    return required_lights, buttons, required_joltage


def parse_machines(lines: Iterator[str]) -> Iterator[tuple[list[bool], list[set[int]], list[int]]]:
    for line in lines:
        yield parse_machine(line)


def button_press_result(num_lights: int, buttons_presses: tuple[set[int], ...]) -> list[bool]:
    rv: list[bool] = [False] * num_lights
    for button in buttons_presses:
        for light_index in button:
            rv[light_index] = not rv[light_index]
    return rv


def is_correct_press_combination(required_lights: list[bool], buttons_presses: tuple[set[int], ...]):
    result: list[bool] = button_press_result(len(required_lights), buttons_presses)
    return required_lights == result


def fewest_presses(required_lights: list[bool], buttons: list[set[int]]) -> int:
    for presses in itertools.count(0):
        for combination in itertools.combinations(buttons, presses):
            if is_correct_press_combination(required_lights, combination):
                return presses
    raise AssertionError


def solve10(lines: Iterator[str]) -> Iterator[int]:

    part1: int = 0

    required_lights: list[bool]
    buttons: list[set[int]]
    required_joltage: list[int]
    for required_lights, buttons, required_joltage in parse_machines(lines):
        part1 += fewest_presses(required_lights, buttons)

    yield part1
    yield 0
