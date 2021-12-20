import itertools


def neighbors(y, x):
    for dy, dx in itertools.product((-1, 0, 1), repeat=2):
        yield (y + dy, x + dx)


def calc_output_pixel(y, x, img, enha_algo, default):
    enha_idx = sum(
        (1 if img.get(neighbor, default) == '#' else 0) << (8 - pos)
        for pos, neighbor in enumerate(neighbors(y, x))
    )
    return enha_algo[enha_idx]


def minmax(img):
    (_, minx), (_, maxx) = min(img.keys(), key=lambda kv: kv[1]), max(
        img.keys(), key=lambda kv: kv[1])
    (miny, _), (maxy, _) = min(img.keys(), key=lambda kv: kv[0]), max(
        img.keys(), key=lambda kv: kv[0])
    return (miny, maxy), (minx, maxx)


def loop(img, offset):
    (miny, maxy), (minx, maxx) = minmax(img)

    OFFSET = offset
    for y in range(miny - OFFSET, maxy + OFFSET + 1):
        for x in range(minx - OFFSET, maxx + OFFSET + 1):
            yield (y, x)


def count_lit_pixels(enha_algo, input_img, n_rounds):
    img = {
        (y, x): input_img[y][x]
        for y in range(len(input_img))
        for x in range(len(input_img[0]))
    }
    for i in range(n_rounds):
        next_img = {}
        default = '.' if i % 2 == 0 else '#'
        for (y, x) in loop(img, 1):
            next_img[(y, x)] = calc_output_pixel(
                y, x, img, enha_algo, default)
        img = next_img

    return sum(1 for pos in loop(img, 0) if img[pos] == '#')


def part1(enha_algo, input_img):
    return count_lit_pixels(enha_algo, input_img, n_rounds=2)


def part2(enha_algo, input_img):
    return count_lit_pixels(enha_algo, input_img, n_rounds=50)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        enha_algo_blk, input_img_blk = f.read().split('\n\n')
        enha_algo = ''.join(enha_algo_blk.split('\n'))
        input_img = input_img_blk.split('\n')

    print(part1(enha_algo, input_img))
    print(part2(enha_algo, input_img))
