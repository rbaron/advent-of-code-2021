
from typing import final


def part1(grid):
    h = len(grid)
    w = len(grid[0])

    def step(grid):
        new_grid = [['.' for _ in range(w)] for _ in range(h)]
        for y, row in enumerate(grid):
            for x, spot in enumerate(row):
                if spot == '>':
                    tentative_new_x = (x + 1) % w
                    if grid[y][tentative_new_x] == '.':
                        new_grid[y][tentative_new_x] = spot
                    else:
                        new_grid[y][x] = spot
        final_grid = new_grid[:]
        for y, row in enumerate(grid):
            for x, spot in enumerate(row):
                if spot == 'v':
                    tentative_new_y = (y + 1) % h
                    if new_grid[tentative_new_y][x] == '.' and grid[tentative_new_y][x] != 'v':
                        final_grid[tentative_new_y][x] = spot
                    else:
                        final_grid[y][x] = spot
        return final_grid

    round = 0
    while True:
        new_grid = step(grid)
        if new_grid == grid:
            return round + 1
        grid = new_grid
        round += 1


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        grid = [list(l.strip()) for l in f]

    print(part1(grid))
