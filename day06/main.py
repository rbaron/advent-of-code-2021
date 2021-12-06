
N_DAYS = 256
CYCLE = 7
EXTRA = 2


def part1(states):
    new = states[:]
    for _ in range(N_DAYS):
        for i, s in enumerate(states):
            if s == 0:
                new[i] = CYCLE - 1
                new.append(CYCLE + EXTRA - 1)
            else:
                new[i] -= 1
        states = new
        new = states[:]
    print(len(new))


def part2(states):
    cache = {}

    def count_descendants(state):
        if state in cache:
            return cache[state]

        n_descendants = 0
        day = state
        while day < N_DAYS:
            n_descendants += 1 + \
                count_descendants(day + CYCLE + EXTRA)
            day += CYCLE

        cache[state] = n_descendants
        return n_descendants

    print(sum(1 + count_descendants(state) for state in states))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        states = list(map(int, next(f).split(',')))

    # part1(states)
    part2(states)
