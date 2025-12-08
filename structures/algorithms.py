from collections import defaultdict


class UnionFind:

    __slots__ = ['parents', 'sizes', 'count']

    def __init__(self, num_ints: int) -> None:
        self.parents: list[int] = list(range(num_ints))
        self.sizes: int[int] = [1] * num_ints
        self.count: int = num_ints

    def find(self, item: int) -> int:
        root: int = item
        while self.parents[root] != root:
            root = self.parents[root]
        while self.parents[item] != root:
            parent: int = self.parents[item]
            self.parents[item] = root
            item = parent
        return root

    def union(self, x: int, y: int) -> bool:
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.sizes[x] < self.sizes[y]:
            x, y = y, x
        self.parents[y] = x
        self.count -= 1
        self.sizes[x] = self.sizes[x] + self.sizes[y]
        return True

    def __len__(self) -> int:
        return self.count

    def to_sets(self) -> list[set[int]]:
        rv: dict[int, set[int]] = defaultdict(set)
        for item in self.parents:
            rv[self.find(item)].add(item)
        return list(rv.values())

    def set_sizes(self):
        num_ints: int = len(self.parents)
        seen_roots: list[bool] = [False] * num_ints
        rv: list[int] = []
        for element in range(num_ints):
            root: int = self.find(element)
            if not seen_roots[root]:
                seen_roots[root] = True
                rv.append(self.sizes[root])
        return rv
