from collections import defaultdict
import itertools
from functools import cache
import math


def find_valid_speeds(target_area):
    (minx, maxx), (miny, maxy) = target_area

    def simy(vy0):
        max_y = 0
        y = 0
        vy = vy0
        t = 0
        while y >= miny:
            if miny <= y <= maxy:
                yield (vy0, t, max_y)
            y += vy
            max_y = max(max_y, y)
            vy -= 1
            t += 1

    def simx(vx0, t):
        x = 0
        vx = vx0
        for _ in range(t):
            x += vx
            vx = max(vx - 1, 0)
        if minx <= x <= maxx:
            yield vx0

    valid_vy0 = [sol for vy0 in range(-500, 500)
                 for sol in simy(vy0)]

    def group_by_t(valid):
        vs_by_t = defaultdict(list)
        for v, t, max_y in valid:
            vs_by_t[t].append((v, max_y))
        return vs_by_t

    valid_initial_speeds = []
    for t, vys in group_by_t(valid_vy0).items():
        for vx0 in range(500):
            for vx in simx(vx0, t):
                for vy in vys:
                    valid_initial_speeds.append((vx, vy[0], vy[1]))

    return set(valid_initial_speeds)


def part1(target_area):
    return max(max_y for _, _, max_y in find_valid_speeds(target_area))


def part2(target_area):
    return len(find_valid_speeds(target_area))


if __name__ == '__main__':
    # Test input.
    # target_area = [(20, 30), (-10, -5)]
    # Real input.
    target_area = [(257, 286), (-101, -57)]

    print(part1(target_area))
    print(part2(target_area))
