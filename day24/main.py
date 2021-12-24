from functools import cache


def run_instrs(input, instrs):
    regs = {'x': 0, 'y': 0, 'z': 0, 'w': 0}

    def eval_val(val):
        if val in regs:
            return regs[val]
        return int(val)

    for op, reg, val in instrs:
        match op:
            case 'inp':
                regs[reg] = input.pop()
                if regs['z'] % 26 != 0:
                    return regs
            case 'add':
                regs[reg] += eval_val(val)
            case 'mul':
                regs[reg] *= eval_val(val)
            case 'div':
                regs[reg] //= eval_val(val)
            case 'mod':
                regs[reg] = regs[reg] % eval_val(val)
            case 'eql':
                regs[reg] = 1 if eval_val(val) == regs[reg] else 0
    return regs


def run_until_inp(instrs, pc, regs):
    def eval_val(val):
        if val in regs:
            return regs[val]
        return int(val)

    while pc < len(instrs):
        op, reg, val = instrs[pc]
        match op:
            case 'inp':
                return regs, pc
            case 'add':
                regs[reg] += eval_val(val)
            case 'mul':
                regs[reg] *= eval_val(val)
            case 'div':
                regs[reg] //= eval_val(val)
            case 'mod':
                regs[reg] = regs[reg] % eval_val(val)
            case 'eql':
                regs[reg] = 1 if eval_val(val) == regs[reg] else 0
        pc += 1

    return regs, pc


def run_level(digit, z, level, instrs):
    pc = 1 + level * 18
    regs = {'z': z, 'w': digit, 'x': 0, 'y': 0}
    new_regs, new_pc = run_until_inp(instrs, pc, regs)
    return new_regs['z']


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
            if z == 0:
                print('ok!')
                return [[]]
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
    print(len(all_sols))

    # Part 1.
    print(''.join(map(str, max(all_sols))))

    # Part 2.
    print(''.join(map(str, min(all_sols))))


if __name__ == '__main__':
    def parse_line(line):
        terms = line.strip().split(' ')
        return terms + [None] * (3 - len(terms))

    with open('input.txt', 'r') as f:
        instrs = [parse_line(l) for l in f]

    # Only three values vary among blocks of instructions between two `inp` instructions.
    # These params are extract here for each block.
    params = [
        (int(instrs[4 + i * 18][2]), int(instrs[5 + i * 18][2]),
         int(instrs[15 + i * 18][2]))
        for i in range(len(instrs) // 18)
    ]

    find_model_numbers(params)
