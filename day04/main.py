import itertools


def rows(board):
    for r in board:
        yield r


def cols(board):
    for c in zip(*board):
        yield c


def get_win_round_by_board(all_drawn_at_round, boards):
    def sequence_first_appears_at_round(seq, lo_idx, hi_idx):
        if hi_idx <= lo_idx + 1:
            return hi_idx if all_drawn_at_round[hi_idx].issuperset(seq) else -1
        else:
            mid = (lo_idx + hi_idx) // 2
            if all_drawn_at_round[mid].issuperset(seq):
                return sequence_first_appears_at_round(seq, lo_idx, mid)
            else:
                return sequence_first_appears_at_round(seq, mid, hi_idx)

    return {
        idx: min(
            sequence_first_appears_at_round(
                set(s), 0, len(all_drawn_at_round)-1)
            for s in itertools.chain(rows(board), cols(board)))
        for idx, board in enumerate(boards)
    }


def score(board, all_drawn, last_drawn):
    return last_drawn * sum(n for r in board for n in r if n not in all_drawn)


def main():
    with open('input.txt', 'r') as f:
        drawn_numbers = [int(n) for n in next(f).split(',')]
        boards = [
            [[int(n) for n in line.split(' ') if n]
             for line in block.strip().split('\n')]
            for block in f.read().split('\n\n')
        ]

    all_drawn_at_round = [set() for _ in drawn_numbers]
    all_drawn_at_round[0] |= {drawn_numbers[0]}
    for i in range(1, len(drawn_numbers)):
        all_drawn_at_round[i] = all_drawn_at_round[i-1] | {drawn_numbers[i]}

    win_round_by_board = get_win_round_by_board(all_drawn_at_round, boards)

    # Part 1.
    p1_board_idx, p1_won_at_round = min(
        win_round_by_board.items(), key=lambda kv: kv[1])
    print(score(boards[p1_board_idx], all_drawn_at_round[p1_won_at_round],
          drawn_numbers[p1_won_at_round]))

    # Part 2.
    p2_board_idx, p2_won_at_round = max(
        win_round_by_board.items(), key=lambda kv: kv[1])
    print(score(boards[p2_board_idx], all_drawn_at_round[p2_won_at_round],
          drawn_numbers[p2_won_at_round]))


if __name__ == '__main__':
    main()
