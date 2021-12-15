import itertools
from functools import cache
import sys
import heapq


def min_risk_path(risk_levels, n_tiles):
    h, w = len(risk_levels), len(risk_levels[0])

    @cache
    def get_risk(n):
        y, x = n
        mult_y, orig_y = divmod(y, h)
        mult_x, orig_x = divmod(x, w)
        e = (risk_levels[orig_y][orig_x] + mult_y + mult_x)
        if e > 9:
            return (e % 10) + 1
        else:
            return e

    def neighbors(n):
        y, x = n
        for (dy, dx) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            ny, nx = y + dy, x + dx
            if not dy == dx == 0 and 0 <= ny < n_tiles * h and 0 <= nx < n_tiles * w:
                yield ny, nx

    end_node = (n_tiles * h - 1, n_tiles * w - 1)
    start_node = (0, 0)
    visited = set()

    queue = [(0, start_node)]
    while entry := heapq.heappop(queue):
        cost, node = entry
        if node == end_node:
            return cost
        elif node in visited:
            continue
        visited.add(node)
        for n in neighbors(node):
            heapq.heappush(queue, (cost + get_risk(n), n))


def part1(risk_levels):
    return min_risk_path(risk_levels, n_tiles=1)


def part2(risk_levels):
    return min_risk_path(risk_levels, n_tiles=5)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        risk_levels = [list(map(int, l.strip())) for l in f]

    print(part1(risk_levels))
    print(part2(risk_levels))
