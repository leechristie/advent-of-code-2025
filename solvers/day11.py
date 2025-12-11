from typing import Iterator


__all__ = ['solve11']


def parse_device(line: str, devices: dict[str, set[str]]) -> None:
    device_id, outputs = line.split(': ')
    devices[device_id] = set(outputs.split(' '))


def parse_devices_str(lines: Iterator[str]) -> dict[str, set[str]]:
    rv: dict[str, set[str]] = {}
    for line in lines:
        parse_device(line, rv)
    return rv


def parse_devices(lines: Iterator[str], poi: tuple[str, ...]) -> tuple[dict[int, tuple[int, ...]], int, tuple[int, ...]]:
    devices_str: dict[str, set[str]] = parse_devices_str(lines)
    devices: dict[int, tuple[int, ...]] = {}
    strings_to_ints: dict[str, int] = {}
    ints_to_strings: list[str] = []
    for i, s in enumerate(set(devices_str.keys()) | set(poi)):
        ints_to_strings.append(s)
        strings_to_ints[s] = i
    poi_ints: tuple[int, ...] = tuple([strings_to_ints[p] for p in poi])
    for device, outputs in devices_str.items():
        devices[strings_to_ints[device]] = tuple([strings_to_ints[d] for d in outputs])
    return devices, len(strings_to_ints), poi_ints


def solve_part1(DEVICE: dict[int, tuple[int, ...]], NUM_DEVICES: int, YOU: int, OUT: int) -> int:
    memo: list[int] = [-1] * NUM_DEVICES
    def num_paths(start: int) -> int:
        m = memo[start]
        if memo[start] != -1:
            return m
        rv: int = 0
        if start == OUT:
            rv = 1
        else:
            for output in DEVICE[start]:
                rv += num_paths(output)
        memo[start] = rv
        return rv
    return num_paths(YOU)


def solve_part2(DEVICE: dict[int, tuple[int, ...]], NUM_DEVICES: int, SVR: int, DAC: int, FFT: int, OUT: int) -> int:
    memo: list[tuple[int, int, int, int] | None] = [None] * NUM_DEVICES
    def num_paths(start: int) -> tuple[int, int, int, int]:
        m = memo[start]
        if memo[start] is not None:
            return m
        empty: int = 0
        dac: int = 0
        fft: int = 0
        dac_fft: int = 0
        if start == OUT:
            empty += 1
        else:
            for output in DEVICE[start]:
                empty_paths, dac_paths, fft_paths, dac_fft_paths = num_paths(output)
                if start == DAC:
                    dac += empty_paths
                    dac += dac_paths
                    dac_fft += fft_paths
                    dac_fft += dac_fft_paths
                elif start == FFT:
                    fft += empty_paths
                    dac_fft += dac_paths
                    fft += fft_paths
                    dac_fft += dac_fft_paths
                else:
                    empty += empty_paths
                    dac += dac_paths
                    fft += fft_paths
                    dac_fft += dac_fft_paths
        rv: tuple[int, int, int, int] = empty, dac, fft, dac_fft
        memo[start] = rv
        return rv

    _, _, _, rv = num_paths(SVR)
    return rv


def solve11(lines: Iterator[str],
            example_b_lines: Iterator[str] | None = None) -> Iterator[int]:

    devices, num_devices, (you, svr, dac, fft, out) = parse_devices(lines, ('you', 'svr', 'dac', 'fft', 'out'))

    yield solve_part1(devices, num_devices, you, out)

    # puzzle has different Part 2 input for the example :/
    if example_b_lines is not None:
        devices, num_devices, (you, svr, dac, fft, out) = parse_devices(example_b_lines, ('you', 'svr', 'dac', 'fft', 'out'))

    yield solve_part2(devices, num_devices, svr, dac, fft, out)