import itertools
from functools import cache


def part1(pos1, pos2):
    def roll():
        i = 0
        while True:
            yield i + 1
            i = (i + 1) % 100

    def sum3(gen):
        return sum(itertools.islice(gen, 3))

    total_rolls = score1 = score2 = 0
    round = 1
    dice = roll()
    while True:
        pos1 = ((pos1 - 1 + sum3(dice)) % 10) + 1
        score1 += pos1
        if score1 >= 1000:
            total_rolls = 3 + (round - 1) * 6
            break
        pos2 = ((pos2 - 1 + sum3(dice)) % 10) + 1
        score2 += pos2
        if score2 >= 1000:
            total_rolls = round * 6
            break
        round += 1

    return min(score1, score2) * total_rolls


def part2(pos1, pos2):
    @cache
    def play_round(pos1, pos2, score1, score2):
        wins = [0, 0]
        for rolls1 in itertools.product([1, 2, 3], repeat=3):
            roll1 = sum(rolls1)
            new_pos1 = ((pos1 - 1 + roll1) % 10) + 1
            new_score1 = score1 + new_pos1
            if new_score1 >= 21:
                wins[0] += 1
                continue

            for rolls2 in itertools.product([1, 2, 3], repeat=3):
                roll2 = sum(rolls2)
                new_pos2 = ((pos2 - 1 + roll2) % 10) + 1
                new_score2 = score2 + new_pos2
                if new_score2 >= 21:
                    wins[1] += 1
                    continue

                n_1_wins, n_2_wins = play_round(
                    new_pos1, new_pos2, new_score1, new_score2)
                wins[0] += n_1_wins
                wins[1] += n_2_wins
        return tuple(wins)

    return max(play_round(pos1, pos2, 0, 0))


if __name__ == '__main__':
    # pos1, pos2 = 4, 8
    pos1, pos2 = 4, 9
    print(part1(pos1, pos2))
    print(part2(pos1, pos2))
