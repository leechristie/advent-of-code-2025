from __future__ import annotations

from typing import TextIO

from structures.points import Dimensions, Point, Facing


class Grid:

    cells: list[list[str]]
    dimensions: Dimensions
    floor: str | None

    def __init__(self, rows: list[str], floor: str|None=None) -> None:
        assert type(rows) == list and len(rows) > 0
        assert type(floor) == str and len(floor) == 1
        self.floor = floor
        self.cells = []
        width: int | None = None
        for row in rows:
            row_cells: list[str] = []
            assert type(row) == str
            if width is not None:
                assert len(row) == width
            width = len(row)
            assert '\n' not in row
            for cell in row:
                row_cells.append(cell)
            self.cells.append(row_cells)
        assert width is not None
        self.dimensions = Dimensions(width=width, height=len(rows))

    @staticmethod
    def parse(file: TextIO, floor: str|None=None) -> Grid:
        rows: list[str] = []
        for line in file:
            line = line.strip('\n')
            if not line:
                break
            rows.append(line)
        return Grid(rows, floor=floor)

    def __str__(self) -> str:
        rv: str = ''
        for row in self.cells:
            for cell in row:
                rv += cell
            rv += '\n'
        return rv.strip('\n')

    def __setitem__(self, position: Point, symbol: str) -> None:
        assert type(position) == Point
        assert position in self.dimensions
        assert type(symbol) == str and len(symbol) == 1
        self.cells[position.y][position.x] = symbol

    def __getitem__(self, position: Point) -> str:
        assert type(position) == Point
        assert position in self.dimensions
        return self.cells[position.y][position.x]

    def collision_check(self, position: Point) -> bool:
        assert self.floor is not None
        assert type(position) == Point
        assert position in self.dimensions
        return self.cells[position.y][position.x] != self.floor
