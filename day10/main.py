
PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
    '': '',
}


def part1(lines):

    SCORES = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    def eval_syntax(line):
        stack = [0]
        for c in line:
            if c in PAIRS:
                stack.append(c)
            elif c != PAIRS[stack[-1]]:
                return SCORES[c]
            else:
                stack.pop()
        return 0

    return sum(map(eval_syntax, lines))


def part2(lines):

    SCORES = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    def calc_score(stack):
        score = 0
        for c in stack:
            score = 5 * score + SCORES[PAIRS[c]]
        return score

    def eval_syntax(line):
        stack = [0]
        for c in line:
            if c in PAIRS:
                stack.append(c)
            elif c != PAIRS[stack[-1]]:
                return 0
            else:
                stack.pop()
        return calc_score(reversed(stack[1:]))

    # print(eval_syntax('[({(<(())[]>[[{[]{<()<>>'))
    # sccores = sorted([calc_score]
    scores = [eval_syntax(l) for l in lines]
    sorted_scores = sorted(s for s in scores if s > 0)
    # print(sorted_scores[len])
    # print(len(sorted_scores))
    return sorted_scores[len(sorted_scores) // 2]


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = [l.strip() for l in f]

    print(part1(lines))
    print(part2(lines))
