from typing import Iterable
from collections import defaultdict


# TODO: fix the fast version
class UnionFind[T]:
    def __init__(self, items: Iterable[T]) -> None:
        self.sets = [{item} for item in items]
    def union(self, x: T, y: T) -> bool:
        ix = -1
        iy = -1
        for i, s in enumerate(self.sets):
            if x in s:
                ix = i
            if y in s:
                iy = i
        if ix == iy:
            return False
        self.sets[ix].update(self.sets[iy])
        del self.sets[iy]
        return True
    def __len__(self) -> int:
        return len(self.sets)
    def to_sets(self) -> list[set[T]]:
        return self.sets


# TODO: fix the fast version
class IntUnionFind:
    def __init__(self, num_ints: int) -> None:
        self.sets = [{item} for item in range(num_ints)]
    def union(self, x: int, y: int) -> bool:
        ix = -1
        iy = -1
        for i, s in enumerate(self.sets):
            if x in s:
                ix = i
            if y in s:
                iy = i
        if ix == iy:
            return False
        self.sets[ix].update(self.sets[iy])
        del self.sets[iy]
        return True
    def __len__(self) -> int:
        return len(self.sets)
    def to_sets(self) -> list[set[int]]:
        return self.sets

#
# class UnionFind[T]:
#
#     __slots__ = ['parents', 'sizes', 'count']
#
#     def __init__(self, items: Iterable[T]) -> None:
#         self.parents: dict[T, T] = {}
#         self.sizes: dict[T, int] = {}
#         self.count: int = 0
#         for item in items:
#             self.parents[item] = item
#             self.sizes[item] = 1
#             self.count += 1
#
#     def find(self, item: T) -> T:
#         root: T = item
#         while self.parents[root] != root:
#             root = self.parents[root]
#         while self.parents[item] != root:
#             parent: T = self.parents[item]
#             self.parents[item] = root
#             item = parent
#         return root
#
#     def union(self, x: T, y: T) -> bool:
#         x = self.find(x)
#         y = self.find(y)
#         if x == y:
#             return False
#         if self.sizes[x] < self.sizes[y]:
#             x, y = y, x
#         self.parents[y] = x
#         self.count -= 1
#         self.sizes[x] = self.sizes[x] + self.sizes[y]
#         return True
#
#     def __len__(self) -> int:
#         return self.count
#
#     def to_sets(self) -> list[set[T]]:
#         rv: dict[int, set[T]] = defaultdict(set)
#         for item in self.parents:
#             rv[self.find(item)].add(item)
#         return list(rv.values())
