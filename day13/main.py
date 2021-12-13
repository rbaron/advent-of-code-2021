
def fold(dots, folds):
    xs, ys = zip(*dots)
    width, height = max(xs) + 1, max(ys) + 1
    grid = [[False] * width for _ in range(height)]
    for x, y in dots:
        grid[y][x] = True

    for axis, coord in folds:
        if axis == 'y':
            for y in range(coord + 1, height):
                for x in range(width):
                    grid[2*coord - y][x] |= grid[y][x]
            height = coord
        else:
            for y in range(height):
                for x in range(coord + 1, width):
                    grid[y][2*coord - x] |= grid[y][x]
            width = coord

    return [r[:width] for r in grid[:height]]


def part1(dots, folds):
    grid = fold(dots, folds[:1])
    return sum(c for r in grid for c in r)


def part2(dots, folds):
    grid = fold(dots, folds)
    for r in grid:
        print(''.join(['#' if c else '.' for c in r]))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        dots_blk, folds_blk = f.read().split('\n\n')
        dots = [tuple(map(int, l.split(','))) for l in dots_blk.split('\n')]
        folds = [('y' if 'y' in l else 'x', int(l.split('=')[1]))
                 for l in folds_blk.split('\n')]

    print(part1(dots, folds))
    part2(dots, folds)
