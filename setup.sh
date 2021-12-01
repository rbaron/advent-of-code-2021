#!/bin/bash
set -eux -o pipefail

DIR=`printf day%02d $1`

mkdir "${DIR}"

cat > "${DIR}/main.py"  <<- EOF

def main():
    print("Hello, world")


if __name__ == '__main__':
    main()
EOF