from collections import namedtuple
from math import prod
import operator

Packet = namedtuple('Packet', 'version type_id size contents')


def sum_versions(packet: Packet):
    if packet.type_id == 4:
        return packet.version
    else:
        return packet.version + sum(sum_versions(p) for p in packet.contents)


def parse_literal(version, type_id, payload):
    ptr = 0
    val = ''
    while True:
        val += payload[ptr+1:ptr+1+4]
        if payload[ptr] == '0':
            return Packet(version, type_id, size=3 + 3 + ptr + 5, contents=int(val, base=2))
        ptr += 5


def parse_operator(version, type_id, payload):
    length_type_id = int(payload[0], base=2)

    subpackets = []

    if length_type_id == 0:
        expected_size = int(payload[1:1+15], base=2)
        ptr = 0
        while ptr < expected_size:
            packet = parse_packet(payload[15+1+ptr:])
            ptr += packet.size
            subpackets.append(packet)
        return Packet(version,
                      type_id,
                      contents=subpackets,
                      size=3 + 3 + 1 + 15 + sum(p.size for p in subpackets))

    elif length_type_id == 1:
        n_subpackets = int(payload[1:1+11], base=2)
        ptr = 0
        for _ in range(n_subpackets):
            packet = parse_packet(payload[11+1+ptr:])
            ptr += packet.size
            subpackets.append(packet)
        return Packet(version,
                      type_id,
                      contents=subpackets,
                      size=3 + 3 + 1 + 11 + sum(p.size for p in subpackets))


def parse_packet(bits):
    version = int(bits[:3], base=2)
    type_id = int(bits[3:6], base=2)
    payload = bits[6:]

    if type_id == 4:
        return parse_literal(version, type_id, payload)
    else:
        return parse_operator(version, type_id, payload)


def eval_packet(packet: Packet):
    def reduce_packet(op):
        return op(eval_packet(p) for p in packet.contents)

    def bin_op(op):
        return 1 if op(eval_packet(packet.contents[0]), eval_packet(packet.contents[1])) else 0

    match packet.type_id:
        case 4:
            return packet.contents
        case 0:
            return reduce_packet(sum)
        case 1:
            return reduce_packet(prod)
        case 2:
            return reduce_packet(min)
        case 3:
            return reduce_packet(max)
        case 5:
            return bin_op(operator.gt)
        case 6:
            return bin_op(operator.lt)
        case 7:
            return bin_op(operator.eq)


def part1(bits):
    return sum_versions(parse_packet(bits))


def part2(bits):
    return eval_packet(parse_packet(bits))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        hex_ = f.read()
        bits = bin(int(hex_.strip(), base=16))[2:]

    # Hack to re-add the leading 0s.
    bits = '0' * (len(hex_) * 4 - len(bits)) + bits

    print(part1(bits))
    print(part2(bits))
