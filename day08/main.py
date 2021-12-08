import collections
import itertools


def part1(outputs):
    print(sum(1 for os in outputs for o in os if len(o) in [2, 3, 4, 7]))


def part2(all_unique_sigs, all_outputs):
    ''' Segment coordinate system:

      000
     5   1
     5   1
      666
     4   2
     4   2
      333
    '''
    def decode(sig_by_segment, output):
        segment_by_sig = {
            next(iter(sig)): seg for seg, sig in sig_by_segment.items()
        }
        segments = {segment_by_sig[sig] for sig in output}
        if segments == {0, 1, 2, 3, 4, 5}:
            return 0
        elif segments == {1, 2}:
            return 1
        elif segments == {0, 1, 3, 4, 6}:
            return 2
        elif segments == {0, 1, 2, 3, 6}:
            return 3
        elif segments == {1, 2, 5, 6}:
            return 4
        elif segments == {0, 2, 3, 5, 6}:
            return 5
        elif segments == {0, 2, 3, 4, 5, 6}:
            return 6
        elif segments == {0, 1, 2}:
            return 7
        elif segments == {0, 1, 2, 3, 4, 5, 6}:
            return 8
        elif segments == {0, 1, 2, 3, 5, 6}:
            return 9
        else:
            raise RuntimeError(f'Invalid segment set: {segments}')

    def solve_line(unique_sigs, outputs):
        possible_mapping = {i: set('abcdefg') for i in range(7)}
        sig_by_len = itertools.groupby(sorted(unique_sigs, key=len), key=len)
        for l, sigs in sig_by_len:
            counts_by_sig = collections.Counter(d for s in sigs for d in s)
            sigs_by_count = collections.defaultdict(set)
            for s, c in counts_by_sig.items():
                sigs_by_count[c] |= set(s)

            if l == 2:
                possible_mapping[1] &= sigs_by_count[1]
                possible_mapping[2] &= sigs_by_count[1]
            elif l == 3:
                possible_mapping[0] &= sigs_by_count[1]
                possible_mapping[1] &= sigs_by_count[1]
                possible_mapping[2] &= sigs_by_count[1]
            elif l == 4:
                possible_mapping[1] &= sigs_by_count[1]
                possible_mapping[2] &= sigs_by_count[1]
                possible_mapping[5] &= sigs_by_count[1]
                possible_mapping[6] &= sigs_by_count[1]
            elif l == 5:
                possible_mapping[0] &= sigs_by_count[3]
                possible_mapping[1] &= sigs_by_count[2]
                possible_mapping[2] &= sigs_by_count[2]
                possible_mapping[3] &= sigs_by_count[3]
                possible_mapping[4] &= sigs_by_count[1]
                possible_mapping[5] &= sigs_by_count[1]
                possible_mapping[6] &= sigs_by_count[3]
            elif l == 6:
                possible_mapping[0] &= sigs_by_count[3]
                possible_mapping[1] &= sigs_by_count[2]
                possible_mapping[2] &= sigs_by_count[3]
                possible_mapping[3] &= sigs_by_count[3]
                possible_mapping[4] &= sigs_by_count[2]
                possible_mapping[5] &= sigs_by_count[3]
                possible_mapping[6] &= sigs_by_count[2]

        # I noticed that after all this filtering, the segment 3 always remains with two
        # possibilities, and one of them is always the one uniquely assigned to segment 0.
        # There is probably something wrong with my code, but this could also be because of
        # the 180 degree symmetry of the problem: if we rotate our display by 180 degrees,
        # it still produces the expected results correct.
        # In my coord system, segment 0 and segment 3 are the the top and bottom horizontal
        # segment, which adds to this evidence.
        possible_mapping[3] -= possible_mapping[0]
        return sum(10**i * decode(possible_mapping, output) for i, output in enumerate(reversed(outputs)))

    print(sum(solve_line(unique_sigs, outputs)
          for unique_sigs, outputs in zip(all_unique_sigs, all_outputs)))


if __name__ == '__main__':
    def parse_line(line):
        uniq_sigs, output = line.split(" | ")
        return (uniq_sigs.strip().split(' '), output.strip().split(' '))

    with open('input.txt', 'r') as f:
        input_data = [parse_line(l) for l in f]

    unique_sigs, outputs = zip(*input_data)
    part1(outputs)
    part2(unique_sigs, outputs)
