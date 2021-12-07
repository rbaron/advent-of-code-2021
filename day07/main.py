
def part1(positions):
    print(min((sum(abs(p - pos) for pos in positions))
          for p in range(min(positions), max(positions) + 1)))


def part2(positions):
    def fuel(p0, p1):
        steps = abs(p1 - p0)
        return steps*(steps + 1) // 2

    print(min((sum(fuel(p, pos) for pos in positions)
          for p in range(min(positions), max(positions) + 1))))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        positions = list(map(int, next(f).split(',')))

    part1(positions)
    part2(positions)
