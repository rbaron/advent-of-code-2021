#!/bin/bash
set -eux -o pipefail

DIR=`printf day%02d $1`
INPUT_NAME=${2:-input_data}

mkdir "${DIR}"
touch "${DIR}/test-input.txt"
touch "${DIR}/input.txt"
cat > "${DIR}/main.py"  <<- EOF

def part1(${INPUT_NAME}):
    return ${INPUT_NAME}


def part2(${INPUT_NAME}):
    pass


if __name__ == '__main__':
    with open('test-input.txt', 'r') as f:
        ${INPUT_NAME} = [int(l) for l in f]

    print(part1(${INPUT_NAME}))
    print(part2(${INPUT_NAME}))

EOF