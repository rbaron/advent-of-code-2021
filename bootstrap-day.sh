#!/bin/bash
set -eux -o pipefail

DIR=`printf day%02d $1`

mkdir "${DIR}"
touch "${DIR}/test-input.txt"
touch "${DIR}/input.txt"
cat > "${DIR}/main.py"  <<- EOF

def part1(input_data):
    pass


def part2(input_data):
    pass


if __name__ == '__main__':
    with open('test-input.txt', 'r') as f:
        input_data = [int(l) for l in f]

    part1(input_data)
    part2(input_data)

EOF