from collections import defaultdict


def part1(target_area):
    _, (miny, maxy) = target_area

    total_max_y = 0
    for v0y in range(miny, -miny+1):
        max_y = y = t = 0
        vy = v0y
        while y >= miny:
            if miny <= y <= maxy:
                total_max_y = max(total_max_y, max_y)
            y += vy
            max_y = max(max_y, y)
            vy -= 1
            t += 1
    return total_max_y


def part2(target_area):
    (minx, maxx), (miny, maxy) = target_area

    y_solutions = defaultdict(set)

    # Simulate y.
    for v0y in range(miny, -miny+1):
        y = t = 0
        vy = v0y
        while y >= miny:
            if miny <= y <= maxy:
                y_solutions[t].add(v0y)
            y += vy
            vy -= 1
            t += 1

    # For each t that satisfies the y constraint, check whether
    # or not it also satisfies the x constraint.
    x_solutions = defaultdict(set)
    for ty in y_solutions:
        for vx0 in range(maxx+1):
            x = 0
            vx = vx0
            for _ in range(ty):
                x += vx
                vx = max(vx-1, 0)
            if minx <= x <= maxx:
                x_solutions[ty].add(vx0)

    combinations = set(
        (vx0, vy0)
        for t, y_sols in y_solutions.items()
        for vy0 in y_sols
        for vx0 in x_solutions[t]
    )

    return len(combinations)


if __name__ == '__main__':
    # Test input.
    # target_area = [(20, 30), (-10, -5)]
    # Real input.
    target_area = [(257, 286), (-101, -57)]

    print(part1(target_area))
    print(part2(target_area))
