from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Dimensions:

    width: int
    height: int

    def __init__(self, *, width: int, height: int) -> None:
        assert type(width) == int and width > 0
        assert type(height) == int and height > 0
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f'{self.width}x{self.height}'

    def __contains__(self, point: Point) -> bool:
        assert type(point) == Point
        return point == point % self


@dataclass
class Point:

    ORIGIN: ClassVar[Point]

    x: int
    y: int

    def __init__(self, *, x: int, y:int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'Point(x={self.x}, y={self.y})'

    def __add__(self, other: Velocity | Facing) -> Point:
        return Point(x=self.x+other.dx, y=self.y+other.dy)

    def __sub__(self, other: Point) -> Velocity:
        return Velocity(dx=self.x-other.x, dy=self.y-other.y)

    def __mod__(self, other: Dimensions) -> Point:
        return Point(x=self.x%other.width, y=self.y%other.height)

    def squared_euclidean(self, other: Point):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def neighbours(self):
        yield Point(x=self.x-1, y=self.y-1)
        yield Point(x=self.x-1, y=self.y)
        yield Point(x=self.x-1, y=self.y+1)
        yield Point(x=self.x, y=self.y-1)
        yield Point(x=self.x, y=self.y+1)
        yield Point(x=self.x+1, y=self.y-1)
        yield Point(x=self.x+1, y=self.y)
        yield Point(x=self.x+1, y=self.y+1)


Point.ORIGIN = Point(x=0, y=0)


class Point3D:

    ORIGIN: ClassVar[Point3D]

    def __init__(self, *, x: int, y:int, z:int) -> None:
        assert type(x) == int
        assert type(y) == int
        assert type(z) == int
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def __repr__(self) -> str:
        return f'Point3D(x={self.x}, y={self.y}, z={self.z})'

    def squared_euclidean(self, other: Point3D):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    x: int
    y: int


Point3D.ORIGIN = Point3D(x=0, y=0, z=0)


@dataclass
class Velocity:

    ZERO: ClassVar[Velocity]

    dx: int
    dy: int

    def __init__(self, *, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def __str__(self) -> str:
        return '{' + f'{self.dx}, {self.dy}' + '}'

    def __repr__(self) -> str:
        return f'Velocity(dx={self.dx}, dy={self.dy})'

    def clockwise90(self) -> Velocity:
        return Velocity(dx=-self.dy, dy=self.dx)

    def counterclockwise90(self) -> Velocity:
        return Velocity(dx=self.dy, dy=-self.dx)

    def __neg__(self) -> Velocity:
        return Velocity(dx=-self.dx, dy=-self.dy)


Velocity.ZERO = Velocity(dx=0, dy=0)


@dataclass
class Facing:

    NORTH: ClassVar[Facing]
    NORTHEAST: ClassVar[Facing]
    EAST: ClassVar[Facing]
    SOUTHEAST: ClassVar[Facing]
    SOUTH: ClassVar[Facing]
    SOUTHWEST: ClassVar[Facing]
    WEST: ClassVar[Facing]
    NORTHWEST: ClassVar[Facing]
    ALL: ClassVar[tuple[Facing, ...]]

    dx: int
    dy: int

    def __init__(self, *, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def as_velocity(self) -> Velocity:
        return Velocity(dx=self.dx, dy=self.dy)

    def clockwise90(self) -> Facing:
        return Facing(dx=-self.dy, dy=self.dx)

    def counterclockwise90(self) -> Facing:
        return Facing(dx=self.dy, dy=-self.dx)

    def __neg__(self) -> Facing:
        return Facing(dx=-self.dx, dy=-self.dy)

    def __repr__(self):
        return f'Facing(dx={self.dx}, dy={self.dy})'

    def __str__(self) -> str:
        if self.dx == -1:
            if self.dy == -1:
                return '↖'
            elif self.dy == 0:
                return '←'
            else:
                assert self.dy == 1
                return '↙'
        elif self.dx == 0:
            if self.dy == -1:
                return '↑'
            else:
                assert self.dy == 1
                return '↓'
        else:
            assert self.dx == 1
            if self.dy == -1:
                return '↗'
            elif self.dy == 0:
                return '→'
            else:
                assert self.dy == 1
                return '↘'


Facing.NORTH = Facing(dx=0, dy=-1)
Facing.NORTHEAST = Facing(dx=1, dy=-1)
Facing.EAST = Facing(dx=1, dy=0)
Facing.SOUTHEAST = Facing(dx=1, dy=1)
Facing.SOUTH = Facing(dx=0, dy=1)
Facing.SOUTHWEST = Facing(dx=-1, dy=1)
Facing.WEST = Facing(dx=-1, dy=0)
Facing.NORTHWEST = Facing(dx=-1, dy=-1)
Facing.ALL = (Facing.NORTH, Facing.NORTHEAST, Facing.EAST, Facing.SOUTHEAST,
              Facing.SOUTH, Facing.SOUTHWEST, Facing.WEST, Facing.NORTHWEST)
