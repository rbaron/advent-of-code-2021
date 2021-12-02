import itertools


def part1(depths):
    print(sum(
        1 if (depths[i] > depths[i-1]) else 0
        for i in range(1, len(depths))
    ))


def part2(depths):
    summed = [
        sum(depths[i:i+3])
        for i in range(0, len(depths) - 2)
    ]
    part1(summed)


def main():
    with open('input.txt', 'r') as f:
        input_data = [int(l) for l in f]

    part1(input_data)
    part2(input_data)


if __name__ == '__main__':
    main()
