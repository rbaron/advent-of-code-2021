from functools import cache
import re
from collections import defaultdict, namedtuple
import sys

RANGE_PATT = '([-+]?\d+)..([-+]?\d+)'
STEP_PATT = re.compile(
    f'(on|off) x={RANGE_PATT},y={RANGE_PATT},z={RANGE_PATT}')


Step = namedtuple('Step', 'on xrange yrange zrange')


def part1(steps):
    reactor = defaultdict(int)
    for step in steps:
        for x in range(step.xrange[0], step.xrange[1] + 1):
            for y in range(step.yrange[0], step.yrange[1] + 1):
                for z in range(step.zrange[0], step.zrange[1] + 1):
                    reactor[(x, y, z)] = step.on
    return sum(reactor.values())


def splits(r1, r2):
    '''Splits r1 into segments going over r2.'''
    # r1 wraps around r2
    if r1[0] < r2[0] and r1[1] > r2[1]:
        return [(r1[0], r2[0] - 1), (r2[0], r2[1]), (r2[1] + 1, r1[1])]
    # r1 overlaps to the left of r2
    elif r1[0] < r2[0] <= r1[1]:
        return [(r1[0], r2[0] - 1), (r2[0], r1[1])]
    # r1 overlaps to the right of r2
    elif r1[0] <= r2[1] < r1[1]:
        return [(r1[0], r2[1]), (r2[1] + 1, r1[1])]
    # if r1 is inside r2, or
    elif r1[0] >= r2[0] and r1[1] <= r2[1]:
        return [r1]
    # r1 is completely to the left or right of r2
    else:
        return [r1]


def get_dim_seg(step: Step, dim):
    match dim:
        case 0: return step.xrange
        case 1: return step.yrange
        case 2: return step.zrange


@cache
def volumes(step1, step2, dim=0):
    if dim > 2:
        return [[]]
    results = []
    for split in splits(get_dim_seg(step1, dim), get_dim_seg(step2, dim)):
        for subvols in volumes(step1, step2, dim + 1):
            results.append([split] + subvols)
    return results


def dimension_overlaps(range1, range2):
    # return range1[0] <= range2[0] <= range1[1] or range1[1] <= range2[1] <= range1[1]
    return range2[0] <= range1[0] <= range2[1] \
        or range2[0] <= range1[1] <= range2[1] \
        or range1[0] <= range2[0] <= range1[1] \
        or range1[0] <= range2[1] <= range1[1]


def overlaps(step1: Step, step2: Step):
    return dimension_overlaps(step1.xrange, step2.xrange) and \
        dimension_overlaps(step1.yrange, step2.yrange) and \
        dimension_overlaps(step1.zrange, step2.zrange)


def split_step(step1: Step, step2: Step):
    if not overlaps(step1, step2):
        # print('NOT OVER', step1, step2)
        return [step1]
    vols = volumes(step1, step2)
    return [Step(step1.on, x, y, z) for x, y, z in vols]


def isinside(step1: Step, step2: Step):
    return step1.xrange[0] >= step2.xrange[0] and step1.xrange[1] <= step2.xrange[1] and \
        step1.yrange[0] >= step2.yrange[0] and step1.yrange[1] <= step2.yrange[1] and \
        step1.zrange[0] >= step2.zrange[0] and step1.zrange[1] <= step2.zrange[1]


def count_ons(step: Step):
    if not step.on:
        return 0
    return (step.xrange[1] - step.xrange[0] + 1) * (step.yrange[1] - step.yrange[0] + 1) * (step.zrange[1] - step.zrange[0] + 1)


def split_rec(step, steps):
    if not steps:
        return [step]
    other = steps[0]
    result = []
    for splitted in split_step(step, other):
        if not isinside(splitted, other):
            result.extend(split_rec(splitted, steps[1:]))
    # return [s for s in r result if not isinside(s, step)]
    return result


def part2(steps):
    fixed_regions = [steps[-1]]
    for i, step in enumerate(list(reversed(steps))[1:]):
        print(f'Step {i}')
        new = split_rec(step, fixed_regions)
        # print('new', new)
        fixed_regions.extend(new)

    # print('Final: ')
    # for s in fixed_regions:
    #     print('\t', s)

    #     print('Applying ', step)
    #     new_fixed_regions = fixed_regions[:]
    #     for fixed_region in fixed_regions:
    #         # for volume in volumes(step, fixed_region):
    #         #     new_step = Step(step.on, volume[0], volume[1], volume[2])
    #         for new_step in split_step(step, fixed_region):
    #             # if not isinside(new_step, fixed_region):
    #             if all(not isinside(new_step, other) for other in fixed_regions):
    #                 new_fixed_regions.append(new_step)
    #             # new_fixed_regions.append(new_step)
    #     fixed_regions = new_fixed_regions
    #     # print(i, len(fixed_regions))
    #     print(i, fixed_regions)
    #     # print(i)
    # print('Final: ')
    # for s in fixed_regions:
    #     print('\t', s)
    # print('regs', len(fixed_regions))
    return sum(count_ons(s) for s in fixed_regions)


if __name__ == '__main__':

    def clip(range):
        # return max(int(range[0]), -50), min(int(range[1]), 50)
        return int(range[0]), int(range[1])

    def parse_step(line):

        mg = STEP_PATT.match(line).groups()
        return Step('on' == mg[0], clip(mg[1:3]), clip(mg[3:5]), clip(mg[5:7]))

    with open('input.txt', 'r') as f:
        steps = [parse_step(l) for l in f]

    # steps = [
    #     s for s in steps
    #     if s.xrange[0] <= 50
    #     and s.xrange[1] >= -50
    #     and s.yrange[0] <= 50
    #     and s.yrange[1] >= -50
    #     and s.zrange[0] <= 50
    #     and s.zrange[1] >= -50
    # ]

    # print(steps)
    # print(part1(steps))
    sys.setrecursionlimit(int(1e6))
    print(part2(steps))
    # print(splits((2, 5), (0, 3)))
    # print(split_step(steps[1], steps[0]))
    # print(volumes(steps[1], steps[0]))
    # s1 = steps[-2]
    # s2 = steps[-1]
    # print(f'Splitting {s1} and {s2}')
    # for s in split_step(s1, s2):
    #     print(s)

    # # Equal.
    # assert splits((0, 3), (0, 3)) == [(0, 3)]
    # # Left.
    # assert splits((-2, -1), (0, 3)) == [(-2, -1)]
    # # Right.
    # assert splits((4, 5), (0, 3)) == [(4, 5)]
    # # Fully Inside
    # assert splits((1, 2), (0, 3)) == [(1, 2)]
    # # Wraps around
    # assert splits((-4, 4), (0, 3)) == [(-4, -1), (0, 3), (4, 4)]
    # # Left overlap.
    # assert splits((-2, 1), (0, 3)) == [(-2, -1), (0, 1)]
    # # Right overlap.
    # assert splits((2, 4), (0, 3)) == [(2, 3), (4, 4)]

    # step1 = Step(True, (-5, 15), (0, 10), (0, 10))
    # step2 = Step(True, (0, 10), (0, 10), (0, 10))
    # print(volumes(step1, step2))
