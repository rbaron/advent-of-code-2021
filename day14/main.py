from collections import Counter
from functools import cache
import itertools


def part1(template, rules):
    def make_new_template(template):
        new_template = []
        for p0, p1 in itertools.pairwise(template):
            new_template.extend([p0, rules[(p0, p1)]])
        new_template.append(p1)
        return new_template

    for _ in range(10):
        template = make_new_template(template)
    counter = sorted(Counter(template).values())
    return counter[-1] - counter[0]


def count_elements(template, rules, depth):
    @cache
    def count_elements_inner(pair, depth):
        if depth == 0:
            return Counter(pair)
        new_el = rules[pair]
        return \
            count_elements_inner((pair[0], new_el), depth - 1) + \
            count_elements_inner((new_el, pair[1]), depth - 1) - \
            Counter({new_el: 1})

    counts = sum((count_elements_inner(pair, depth)
                 for pair in itertools.pairwise(template)), start=Counter())
    return counts - Counter(template[1:-1])


def part2(template, rules):
    counts = count_elements(template, rules, 40)
    values = sorted(counts.values())
    return values[-1] - values[0]


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        template_blk, rules_blk = f.read().split('\n\n')
        template = template_blk.strip()
        rules = {
            tuple(patt): char
            for patt, char in [r.split(' -> ') for r in rules_blk.split('\n')]
        }

    print(part1(template, rules))
    print(part2(template, rules))
