import math
import itertools

'''
[[6,[5,[4,[3,2]]]],1]
[
    [
        6,
        [
            5,
            [
                4,
                [
                    3,
                    2
                ]
            ]
        ]
    ],
    1
]

[
    [
        [
            [
                [
                    9,
                    8],
                1],
            2],
        3],
    4]
'''


def print_snailfish_number(n, indent=0):
    if isinstance(n, int):
        print('    ' * indent, n)
        return
    print('    ' * indent, '*')
    print_snailfish_number(n[0], indent+1)
    print_snailfish_number(n[1], indent+1)


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

    def maybe_collapse(node, level, actioned, explode_allowed):
        # if actioned:
        #     return actioned, 0, 0, node

        if isinstance(node, int):
            if explode_allowed and node >= 10:
                return True, 0, 0, (node // 2, math.ceil(node / 2))
            return False, 0, 0, node

        if level == 4:
            return True, node[0], node[1], 0

        collapsed_left, sumleft, sumright, new_node = maybe_collapse(
            node[0], level + 1, actioned, explode_allowed)
        if collapsed_left:
            return True, sumleft, 0, (new_node, addleft(node[1], sumright))

        collapsed_right, sumleft, sumright, new_node = maybe_collapse(
            node[1], level + 1, actioned, explode_allowed)
        if collapsed_right:
            return True, 0, sumright, (addright(node[0], sumleft), new_node)

        return actioned, 0, 0, node

    nn = n
    while True:
        begin_node = nn
        print('Old node: ', nn)
        while True:
            _, _, _, new_node = maybe_collapse(nn, 0, False, False)
            if new_node is nn:
                break
            nn = new_node
        while True:
            _, _, _, new_node = maybe_collapse(nn, 0, False, True)
            if new_node is nn:
                break
            nn = new_node

        if begin_node == nn:
            return begin_node


def parse_snailfish(str, idx):
    ''' Parses the LL(1) grammar:

    SN := [ SN , SN ]
       | number_literal
    '''
    # We have a nested snailfish number.
    if str[idx] == '[':
        left, idx = parse_snailfish(str, idx + 1)
        right, idx = parse_snailfish(str, idx + 1)
        return (left, right), idx + 1
    # We have a literal.
    else:
        idx_last = idx
        while str[idx_last].isdigit():
            idx_last += 1
        # + 1 to consume the comma.
        return int(str[idx:idx_last]), idx_last


def part1(snailfish_numbers):
    # return reduce(snailfish_numbers)
    # print(snailfish_numbers)
    lhs = snailfish_numbers[0]
    for rhs in snailfish_numbers[1:]:
        print(f'  {lhs}')
        print(f'+ {rhs}')
        lhs = reduce(add(lhs, rhs))
        print(f'= {lhs}\n')
    # print(lhs)
    return magnitude(lhs)


def part2(snailfish_numbers):
    return max(magnitude(reduce(add(n1, n2))) for n1, n2 in itertools.product(snailfish_numbers, repeat=2) if n1 != n2)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        # str = f.read().strip()
        snailfish_numbers = [parse_snailfish(l.strip(), 0)[0] for l in f]

    # print_snailfish_number(snailfish_numbers[0])
    print(part1(snailfish_numbers))
    # print(reduce(snailfish_numbers[0]))
    print(part2(snailfish_numbers))

[[[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
    [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]]
# [[[[4,0],[5,4]],[[0,[7,6]],[9,5]]], [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]
