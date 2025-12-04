from __future__ import annotations
import numpy as np
from typing import TextIO, Any, Iterator

from structures.points import Dimensions, Point


class Grid:

    cells: np.ndarray
    dimensions: Dimensions
    symbols: tuple[str, ...]

    def __init__(self, cells: np.ndarray, dimensions: Dimensions, symbols: tuple[str, ...]) -> None:
        self.cells = cells
        self.dimensions = dimensions
        self.symbols = symbols

    @staticmethod
    def parse(file: Iterator[str], symbols: tuple[str, ...] | list[str] | str, unique: str | None = None) -> tuple[Grid, Point | None]:
        num_symbols: int = len(symbols)
        assert (num_symbols >= 2), 'too few symbols'
        assert (num_symbols <= 256), 'too many symbols'
        assert (len(set(symbols)) == num_symbols), 'duplicate in symbols'
        assert ('\n' not in symbols), 'symbols contains new line character'
        if type(symbols) != tuple:
            symbols = tuple(symbols)
        assert type(symbols) == tuple
        for symbol in symbols:
            assert (type(symbol) == str and len(symbol) == 1), f'invalid symbol: {symbol!r}'
        if unique is not None:
            assert (unique in symbols), f'unique symbol {unique!r} no in symbol list'
        unique_location = None
        rows: list[str] = []
        num_cols: int | None = None
        for line in file:
            line = line.strip('\n')
            if not line:
                break
            for symbol in line:
                assert (symbol in symbols), f'unexpected symbol: {symbol!r}'
            rows.append(line)
            if num_cols is not None:
                assert (len(line) == num_cols), ''
            num_cols = len(line)
        num_rows: int = len(rows)
        assert num_rows > 0 and num_cols is not None and num_cols > 0
        cells = np.zeros((num_rows, num_cols), dtype=np.uint8)
        assert type(cells) == np.ndarray and len(cells.shape) == 2 and cells.dtype == np.uint8
        assert cells.shape[0] > 0 and cells.shape[1] > 0
        for y, row in enumerate(rows):
            for x, symbol in enumerate(row):
                try:
                    if symbol == unique:
                        if unique_location is not None:
                            raise AssertionError(f'unique symbol {unique!r} is not unique')
                        unique_location = Point(x=x, y=y)
                    cells[y, x] = symbols.index(symbol)
                except ValueError:
                    raise AssertionError(f'unexpected symbol populating cells: {symbol!r}')
        if unique is not None and unique_location is None:
            raise AssertionError(f'did not find unique symbol {unique!r}')
        return Grid(cells, Dimensions(width=num_cols, height=num_rows), symbols), unique_location

    def __str__(self) -> str:
        rv: str = ''
        for y in range(self.cells.shape[0]):
            for x in range(self.cells.shape[1]):
                rv += self.symbols[self.cells[y, x]]
            rv += '\n'
        return rv.strip('\n')

    def __repr__(self) -> str:
        return f'Grid({self.cells!r}, {self.dimensions!r}, {self.symbols!r})'

    def __getitem__(self, point: Point) -> str:
        assert type(point) == Point and point in self.dimensions
        return self.symbols[self.cells[point.y, point.x]]

    def __setitem__(self, point: Point, symbol: str) -> None:
        assert type(point) == Point and point in self.dimensions
        assert (symbol in self.symbols), f'cannot set to unexpected new symbol {symbol!r}'
        try:
            number: int = self.symbols.index(symbol)
        except ValueError:
            raise AssertionError(f'unexpected symbol populating cells: {symbol!r}')
        self.cells[point.y, point.x] = number

    def __eq__(self, other: Any) -> bool:
        return (type(other) == Grid
                and self.symbols == other.symbols
                and self.dimensions == other.dimensions
                and self.cells.dtype is self.cells.dtype
                and np.array_equal(self.cells, other.cells))

    def copy(self) -> Grid:
        return Grid(self.cells.copy(), self.dimensions, self.symbols)

    def freeze(self) -> FrozenGrid:
        return FrozenGrid(self)

    def positions(self) -> Iterator[Point]:
        for y in range(0, self.dimensions.height):
            for x in range(0, self.dimensions.width):
                yield Point(x=x, y=y)

    def neighbours(self, point: Point) -> Iterator[Point]:
        for neighbour in point.neighbours():
            if neighbour in self.dimensions:
                yield neighbour

    def replace(self, old: str, new: str) -> None:
        try:
            old_number: int = self.symbols.index(old)
        except ValueError:
            raise AssertionError(f'unexpected symbol populating cells: {old!r}')
        try:
            new_number: int = self.symbols.index(new)
        except ValueError:
            raise AssertionError(f'unexpected symbol populating cells: {new!r}')
        for y in range(self.dimensions.height):
            for x in range(self.dimensions.width):
                if self.cells[y, x] == old_number:
                    self.cells[y, x] = new_number

    def count_neighbours(self, point: Point, symbol: str) -> int:
        if point not in self.dimensions:
            raise ValueError(f'invalid point in grid: {point}')
        try:
            number: int = self.symbols.index(symbol)
        except ValueError:
            return 0
        rv: int = 0
        if point.y - 1 >= 0:
            if point.x - 1 >= 0 and self.cells[point.y - 1, point.x - 1] == number:
                rv += 1
            if self.cells[point.y - 1, point.x] == number:
                rv += 1
            if point.x + 1 < self.dimensions.width and self.cells[point.y - 1, point.x + 1] == number:
                rv += 1
        if point.x - 1 >= 0 and self.cells[point.y, point.x - 1] == number:
            rv += 1
        if point.x + 1 < self.dimensions.width and self.cells[point.y, point.x + 1] == number:
            rv += 1
        if point.y + 1 < self.dimensions.height:
            if point.x - 1 >= 0 and self.cells[point.y + 1, point.x - 1] == number:
                rv += 1
            if self.cells[point.y + 1, point.x] == number:
                rv += 1
            if point.x + 1 < self.dimensions.width and self.cells[point.y + 1, point.x + 1] == number:
                rv += 1
        return rv

    def count_non_zero_neighbours(self, point: Point) -> int:
        if point not in self.dimensions:
            raise ValueError(f'invalid point in grid: {point}')
        rv: int = 0
        if point.y - 1 >= 0:
            if point.x - 1 >= 0 and self.cells[point.y - 1, point.x - 1]:
                rv += 1
            if self.cells[point.y - 1, point.x]:
                rv += 1
            if point.x + 1 < self.dimensions.width and self.cells[point.y - 1, point.x + 1]:
                rv += 1
        if point.x - 1 >= 0 and self.cells[point.y, point.x - 1]:
            rv += 1
        if point.x + 1 < self.dimensions.width and self.cells[point.y, point.x + 1]:
            rv += 1
        if point.y + 1 < self.dimensions.height:
            if point.x - 1 >= 0 and self.cells[point.y + 1, point.x - 1]:
                rv += 1
            if self.cells[point.y + 1, point.x]:
                rv += 1
            if point.x + 1 < self.dimensions.width and self.cells[point.y + 1, point.x + 1]:
                rv += 1
        return rv

class FrozenGrid:

    cells: np.ndarray
    dimensions: Dimensions
    symbols: tuple[str, ...]

    def __init__(self, grid: Grid) -> None:
        self.cells = grid.cells.copy()
        self.dimensions = grid.dimensions
        self.symbols = grid.symbols

    def __str__(self) -> str:
        rv: str = ''
        for y in range(self.cells.shape[0]):
            for x in range(self.cells.shape[1]):
                rv += self.symbols[self.cells[y, x]]
            rv += '\n'
        return rv.strip('\n')

    def __repr__(self) -> str:
        return f'Grid({self.cells!r}, {self.dimensions!r}, {self.symbols!r}).freeze()'

    def __getitem__(self, point: Point) -> str:
        assert type(point) == Point and point in self.dimensions
        return self.symbols[self.cells[point.y, point.x]]

    def __hash__(self) -> int:
        return hash((tuple(self.cells.reshape((-1, ))), self.symbols))

    def __eq__(self, other: Any) -> bool:
        return (type(other) == Grid
                and self.symbols == other.symbols
                and self.dimensions == other.dimensions
                and self.cells.dtype is self.cells.dtype
                and np.array_equal(self.cells, other.cells))

    def unfreeze(self) -> Grid:
        return Grid(self.cells, self.dimensions, self.symbols).copy()
