from collections import defaultdict
from functools import lru_cache
from math import prod
import sys


def neighbors(y, x, height, width):
    if y < height - 1:
        yield (y + 1, x)
    if y > 0:
        yield (y - 1, x)
    if x < width - 1:
        yield (y, x + 1)
    if x > 0:
        yield (y, x - 1)


def part1(heights):
    height = len(heights)
    width = len(heights[0])

    visited = set()
    local_mins = []

    def visit(y, x):
        if (y, x) in visited:
            return
        visited.add((y, x))
        if all(heights[y][x] < heights[ny][nx]
               for ny, nx in neighbors(y, x, height, width)):
            local_mins.append(heights[y][x])
        for (ny, nx) in neighbors(y, x, height, width):
            visit(ny, nx)

    visit(0, 0)
    return sum(1 + h for h in local_mins)


def part2(heights):
    height = len(heights)
    width = len(heights[0])

    @lru_cache(maxsize=None)
    def descent(y, x):
        if heights[y][x] == 9:
            return (-1, -1)

        for (ny, nx) in neighbors(y, x, height, width):
            if heights[ny][nx] < heights[y][x]:
                return descent(ny, nx)
        # We're at a local min.
        return (y, x)

    size_by_basin_coords = defaultdict(int)
    for y, _ in enumerate(heights):
        for x, _ in enumerate(heights[y]):
            size_by_basin_coords[descent(y, x)] += 1

    return prod(sorted((size for (y, x), size in size_by_basin_coords.items()
                        if x >= 0), reverse=True)[:3])


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        heights = [[int(n) for n in l.strip()] for l in f]

    # That's showbiz baby
    sys.setrecursionlimit(int(1e6))

    print(part1(heights))
    print(part2(heights))
