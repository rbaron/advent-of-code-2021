import math
import itertools


def add(n1, n2):
    return (n1, n2)


def magnitude(n):
    if isinstance(n, int):
        return n
    return 3 * magnitude(n[0]) + 2 * magnitude(n[1])


def reduce(n):
    def addleft(node, val):
        if isinstance(node, int):
            return node + val
        else:
            return (addleft(node[0], val), node[1])

    def addright(node, val):
        if isinstance(node, int):
            return node + val
        else:
            return (node[0], addright(node[1], val))

    def maybe_explode(node, level):
        if isinstance(node, int):
            return False, 0, 0, node

        if level == 4:
            return True, node[0], node[1], 0

        collapsed_left, sumleft, sumright, new_node = maybe_explode(
            node[0], level + 1)
        if collapsed_left:
            return True, sumleft, 0, (new_node, addleft(node[1], sumright))

        collapsed_right, sumleft, sumright, new_node = maybe_explode(
            node[1], level + 1)
        if collapsed_right:
            return True, 0, sumright, (addright(node[0], sumleft), new_node)

        return False, 0, 0, node

    def maybe_split(node):
        if isinstance(node, int):
            if node >= 10:
                return True, (node // 2, math.ceil(node / 2))
            return False, node

        split_left, new_node = maybe_split(node[0])
        if split_left:
            return True, (new_node, node[1])
        split_right, new_node = maybe_split(node[1])
        if split_right:
            return True, (node[0], new_node)
        return False, node

    def apply_rules_until_no_change(node):
        while True:
            _, _, _, new_number = maybe_explode(node, 0)
            if new_number == node:
                _, new_number = maybe_split(node)
                if new_number == node:
                    return node
            node = new_number

    return apply_rules_until_no_change(n)


def parse_snailfish(str, idx):
    ''' Parses the LL(1) grammar:

    SN := [ SN , SN ]
       | number_literal
    '''
    if str[idx] == '[':
        left, idx = parse_snailfish(str, idx + 1)
        right, idx = parse_snailfish(str, idx + 1)
        # + 1 to consume the ']'.
        return (left, right), idx + 1
    # We have a literal.
    else:
        idx_last = idx
        while str[idx_last].isdigit():
            idx_last += 1
        return int(str[idx:idx_last]), idx_last


def part1(snailfish_numbers):
    lhs = snailfish_numbers[0]
    for rhs in snailfish_numbers[1:]:
        lhs = reduce(add(lhs, rhs))
    return magnitude(lhs)


def part2(snailfish_numbers):
    return max(magnitude(reduce(add(n1, n2)))
               for n1, n2 in itertools.product(snailfish_numbers, repeat=2)
               if n1 != n2)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        snailfish_numbers = [parse_snailfish(l.strip(), 0)[0] for l in f]

    print(part1(snailfish_numbers))
    print(part2(snailfish_numbers))
