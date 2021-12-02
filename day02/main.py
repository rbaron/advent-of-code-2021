from functools import reduce


def part1(instrs):
    hor = depth = 0
    for direction, amount in instrs:
        if direction == 'forward':
            hor += amount
        elif direction == 'down':
            depth += amount
        elif direction == 'up':
            depth -= amount
    print(hor * depth)


def part2(instrs):
    hor = depth = aim = 0
    for direction, amount in instrs:
        if direction == 'forward':
            hor += amount
            depth += aim * amount
        elif direction == 'down':
            aim += amount
        elif direction == 'up':
            aim -= amount
    print(hor * depth)


def main():
    def parse_line(line):
        direction, amount = line.split(' ')
        return direction, int(amount)

    with open('input.txt', 'r') as f:
        input_data = [parse_line(l) for l in f]

    part1(input_data)
    part2(input_data)


if __name__ == '__main__':
    main()
