import operator


def get_most_common_bits(numbers, n_bits, comparison_op):
    counts = [0] * n_bits
    for n in numbers:
        for pos in range(n_bits):
            counts[pos] += 1 if (n & (1 << pos)) else 0
    return [int(comparison_op(c, len(numbers) / 2)) for c in counts]


def negate_bits(number, n_bits):
    return ~number & ((1 << n_bits) - 1)


def part1(numbers, n_bits):
    most_common_bits = get_most_common_bits(numbers, n_bits, operator.gt)
    gamma = sum(b << i for i, b in enumerate(most_common_bits))
    epsilon = negate_bits(gamma, n_bits)
    print(gamma * epsilon)


def apply_bit_criteria(numbers, n_bits, comparison_op):
    remaining = numbers[:]
    for pos in reversed(range(n_bits)):
        most_common_bits = get_most_common_bits(
            remaining, n_bits, comparison_op)
        remaining = [
            r for r in remaining if r & (1 << pos) == most_common_bits[pos] << pos
        ]
        if len(remaining) == 1:
            return remaining[0]


def part2(numbers, n_bits):
    oxygen_generator_rating = apply_bit_criteria(numbers, n_bits, operator.ge)
    co2_scrubber_rating = apply_bit_criteria(numbers, n_bits, operator.lt)
    print(oxygen_generator_rating * co2_scrubber_rating)


def main():
    with open('input.txt', 'r') as f:
        input_data = [l.rstrip() for l in f]

    n_bits = len(input_data[0])
    numbers = [int(l, base=2) for l in input_data]

    part1(numbers, n_bits)
    part2(numbers, n_bits)


if __name__ == '__main__':
    main()
