import itertools


def part1(input_data):
    print(sum(
        1 if (input_data[i] > input_data[i-1]) else 0
        for i in range(1, len(input_data))
    ))


def part2(input_data):
    summed = [
        sum(input_data[i:i+3])
        for i in range(0, len(input_data) - 2)
    ]
    part1(summed)


def main():
    with open('input.txt', 'r') as f:
        input_data = map(int, f.read().splitlines())

    part1(input_data)
    part2(input_data)


if __name__ == '__main__':
    main()
