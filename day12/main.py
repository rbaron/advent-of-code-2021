from collections import defaultdict
from copy import copy


def part1(cavemap):
    def find_paths(cave, visited):
        if cave == 'end':
            return 1
        elif cave in visited:
            return 0
        return sum(find_paths(next_cave, visited | ({cave} if cave.islower() else set()))
                   for next_cave in cavemap[cave])
    return find_paths('start', set())


def part2(cavemap):
    def find_paths(cave, visit_count, has_double_visit):
        if cave == 'end':
            return 1
        elif ((cave == 'start' and visit_count['start'] > 0)
              or (visit_count[cave] == 2)
              or (visit_count[cave] == 1 and has_double_visit)):
            return 0
        new_visit_count = copy(visit_count)
        new_visit_count[cave] += 1 if cave.islower() else 0
        return sum(find_paths(next_cave,
                              new_visit_count,
                              has_double_visit or visit_count[cave] >= 1)
                   for next_cave in cavemap[cave])
    return find_paths('start', defaultdict(int), False)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        edges = [l.strip().split('-') for l in f]

    cavemap = defaultdict(list)
    for from_, to in edges:
        cavemap[from_].append(to)
        cavemap[to].append(from_)

    print(part1(cavemap))
    print(part2(cavemap))
