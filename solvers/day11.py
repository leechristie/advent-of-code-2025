from functools import cache
from typing import Iterator


__all__ = ['solve11']


def parse_device(line: str, devices: dict[str, set[str]]) -> None:
    device_id, outputs = line.split(': ')
    devices[device_id] = set(outputs.split(' '))


def parse_devices(lines: Iterator[str]) -> dict[str, set[str]]:
    rv: dict[str, set[str]] = {}
    for line in lines:
        parse_device(line, rv)
    return rv


def solve_part1(devices: dict[str, set[str]]) -> int:
    @cache
    def num_paths(start: str) -> int:
        rv: int = 0
        if start == 'out':
            rv = 1
        else:
            for output in devices[start]:
                rv += num_paths(output)
        return rv
    return num_paths('you')


def solve_part2(devices: dict[str, set[str]]) -> int:

    @cache
    def num_paths(start: str, indent=0) -> tuple[int, int, int, int]:
        empty: int = 0
        dac: int = 0
        fft: int = 0
        dac_fft: int = 0
        if start == 'out':
            empty += 1
        else:
            for output in devices[start]:
                empty_paths, dac_paths, fft_paths, dac_fft_paths = num_paths(output, indent=indent+1)
                if start == 'dac':
                    dac += empty_paths
                    dac += dac_paths
                    dac_fft += fft_paths
                    dac_fft += dac_fft_paths
                elif start == 'fft':
                    fft += empty_paths
                    dac_fft += dac_paths
                    fft += fft_paths
                    dac_fft += dac_fft_paths
                else:
                    empty += empty_paths
                    dac += dac_paths
                    fft += fft_paths
                    dac_fft += dac_fft_paths
        return empty, dac, fft, dac_fft

    _, _, _, rv = num_paths('svr')
    return rv


def solve11(lines: Iterator[str],
            example_b_lines: Iterator[str] | None = None) -> Iterator[int]:

    devices: dict[str, set[str]]

    devices = parse_devices(lines)
    part1: int = solve_part1(devices)
    assert (part1 in (5, 788)), f'{part1 = }, expected 5 (example) or 788 (input)'
    yield solve_part1(devices)

    # puzzle has different Part 2 input for the example :/
    if example_b_lines is not None:
        devices = parse_devices(example_b_lines)

    part2: int = solve_part2(devices)
    assert ((part1, part2) in ((5, 2), (788, 316291887968000))), f'{part2 = }'
    yield part2