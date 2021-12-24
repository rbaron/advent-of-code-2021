from functools import cache


def run_level_fast(w, z, level, params):
    '''The instructions were extracted by hand from the raw instructions.
    See monad-annotated.txt for deets.'''
    p0, p1, p2 = params[level]
    x = 0 if (w == z % 26 + p1) else 1
    y = 25 * x + 1
    z = (z // p0) * y
    y = (w + p2) * x
    z += y
    return z


def find_model_numbers(params):
    @cache
    def find_solutions(level, z):
        if level == 14:
            return [[]] if z == 0 else []

        results = []
        for digit in range(1, 10):
            new_z = run_level_fast(digit, z, level, params)
            if level == 1:
                print('z ', new_z)
            found_sols = find_solutions(level + 1, new_z)
            for sol in found_sols:
                results.append([digit] + sol)

        return results

    all_sols = find_solutions(0, 0)

    # Part 1.
    print(''.join(map(str, max(all_sols))))

    # Part 2.
    print(''.join(map(str, min(all_sols))))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        instrs = [l.strip().split() for l in f]

    # Only three values vary among blocks of instructions between two `inp` instructions.
    # These params are extract here for each block. They are in lines 4, 5 and 15 in each
    # block.
    params = [
        (int(instrs[4 + i * 18][2]), int(instrs[5 + i * 18][2]),
         int(instrs[15 + i * 18][2]))
        for i in range(len(instrs) // 18)
    ]

    find_model_numbers(params)
