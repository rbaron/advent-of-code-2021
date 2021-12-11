import itertools

N_STEPS = 100


def neighbors(y, x, h, w):
    for dy, dx in itertools.product(range(-1, 2), repeat=2):
        if not (dy == dx == 0) and 0 <= y + dy < h and 0 <= x + dx < w:
            yield (y + dy, x + dx)


def propagate(new_energy_levels, y, x, h, w):
    # This flash has already been propagated once.
    if new_energy_levels[y][x] > 9:
        return
    else:
        new_energy_levels[y][x] += 1
        if new_energy_levels[y][x] > 9:
            for ny, nx in neighbors(y, x, h, w):
                propagate(new_energy_levels, ny, nx, h, w)


def next_state(energy_levels):
    h, w = len(energy_levels), len(energy_levels[0])
    n_flashes = 0
    new_energy_levels = [r[:] for r in energy_levels]
    for y in range(h):
        for x in range(w):
            propagate(new_energy_levels, y, x, h, w)
    for y in range(h):
        for x in range(w):
            if new_energy_levels[y][x] > 9:
                new_energy_levels[y][x] = 0
                n_flashes += 1
    return new_energy_levels, n_flashes


def part1(energy_levels):
    n_flashes = 0
    for _ in range(N_STEPS):
        energy_levels, new_flashes = next_state(energy_levels)
        n_flashes += new_flashes
    return n_flashes


def part2(energy_levels):
    step = 1
    while True:
        energy_levels, _ = next_state(energy_levels)
        if all(e == 0 for r in energy_levels for e in r):
            return step
        step += 1


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        energy_levels = [[int(n) for n in l.strip()] for l in f]

    print(part1(energy_levels))
    print(part2(energy_levels))
