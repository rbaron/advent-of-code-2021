from collections import Counter


def points(seg):
    (x0, y0), (x1, y1) = sorted(seg)
    if x1 == x0:
        return ((x0, y) for y in range(y0, y1 + 1))
    slope = (y1 - y0) // (x1 - x0)
    return ((x0 + i, y0 + i * slope) for i in range(x1 - x0 + 1))


def count_overlaps(segments):
    counter = Counter(p for s in segments for p in points(s))
    return sum(1 for v in counter.values() if v >= 2)


if __name__ == '__main__':
    def parse_segment(line):
        return tuple(tuple(int(k) for k in p.split(',')) for p in line.split(' -> '))

    with open('input.txt', 'r') as f:
        segments = [parse_segment(l) for l in f]

    print(count_overlaps([s for s in segments if
                          s[0][0] == s[1][0] or s[0][1] == s[1][1]]))

    print(count_overlaps(segments))
