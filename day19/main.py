import itertools
from functools import cache
import numpy as np
from numpy.linalg import matrix_power

# https://en.wikipedia.org/wiki/Rotation_matrix
# sin(90) = 1
# cos(90) = 0
ROT_X = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
ROT_Y = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
ROT_Z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])


def rotations(scans):
    def all_rotations_around_axis(positions, rot_matrix):
        for i in range(4):
            positions = positions @ rot_matrix
            yield positions

    # 4 spins around y.
    yield from all_rotations_around_axis(scans, ROT_Y)
    # +90 around z around spin 4 times around x.
    yield from all_rotations_around_axis(scans @ ROT_Z, ROT_X)
    # +270 around around z around spin 4 times around x.
    yield from all_rotations_around_axis(scans @ matrix_power(ROT_Z, 3), ROT_X)
    # +90 around x and spin 4 times around z.
    yield from all_rotations_around_axis(scans @ ROT_X, ROT_Z)
    # +270 around x and spin 4 times around z.
    yield from all_rotations_around_axis(scans @ matrix_power(ROT_X, 3), ROT_Z)
    # +180 around x and spin 4 times around y.
    yield from all_rotations_around_axis(scans @ matrix_power(ROT_X, 2), ROT_Y)


def beacons_in_common(scans1, scans2):
    # Try to translate to every possible pair of beacons and check if we find >= 12 matching differences.
    for i, b1 in enumerate(scans1):
        for j, b2 in enumerate(scans2):
            beacons_coord_b1 = scans1 - b1
            beacons_coord_b2 = scans2 - b2
            common = set(map(tuple, beacons_coord_b1)) & set(
                map(tuple, beacons_coord_b2))
            if len(common) >= 12:
                # Return common beacons in scans1 coordinates, and distance between scans2 and scans1.
                return np.array(list(common)) + b1, b2 - b1
    return set(), 0


def part1(scans):
    # @cache
    def dfs(scanidx, scan, origin, visited):
        if scanidx in visited:
            return set()

        seen = set()
        for i, next_scan in enumerate(scans):
            for next_rotated in rotations(next_scan):
                common, d = beacons_in_common(scan, next_rotated)
                # If found some connection, recurse there.
                if len(common) > 0:
                    seen |= {tuple(c - origin) for c in common}
                    seen |= dfs(i, next_rotated, origin +
                                d, visited | {scanidx})
        return seen

    return len(dfs(0, scans[0], (0, 0, 0), set()))


def part2(scans):
    pass


if __name__ == '__main__':
    def parse_scan_blk(blk):
        return np.array([
            [int(c) for c in l.split(',')]
            for l in blk.split('\n')[1:]])

    with open('test-input.txt', 'r') as f:
        scan_blocks = f.read().split('\n\n')
        scans = [parse_scan_blk(blk) for blk in scan_blocks]

    # vv = scans[0][0]
    # import ipdb
    # ipdb.set_trace()
    # scans = scans[:8]
    print(part1(scans))
    print(part2(scans))
