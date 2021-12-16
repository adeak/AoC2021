from itertools import islice
from math import prod

def day16(inp):
    bits = f'{int(inp.strip(), 16):b}'
    padded_len = -(-len(bits) // 4) * 4
    bits = bits.zfill(padded_len)
    it = iter(bits)

    metadata = parse_packet(it)

    part1, part2 = compute_scores(metadata)

    return part1, part2


def parse_packet(it):
    version_id = int(''.join(islice(it, 3)), 2)
    type_id = int(''.join(islice(it, 3)), 2)

    if type_id == 4:
        # literal
        val = []
        while True:
            flag, *block = islice(it, 5)
            val.append(''.join(block))
            if flag == '0':
                break
        val = int(''.join(val), 2)
        metadata = (version_id, type_id, val)
    else:
        # operator
        flag = next(it)
        if flag == '0':
            length = int(''.join(islice(it, 15)), 2)
            section = ''.join(islice(it, length))
            it_sub = iter(section)
            subpackets = []
            while True:
                try:
                    subpacket = parse_packet(it_sub)
                except ValueError:
                    # failed int('') on next missing header
                    break
                subpackets.append(subpacket)
        else:
            n_packets = int(''.join(islice(it, 11)), 2)
            subpackets = []
            for _ in range(n_packets):
                subpacket = parse_packet(it)
                subpackets.append(subpacket)

        metadata = (version_id, type_id, tuple(subpackets))

    return metadata


def compute_scores(metadata):
    version_id, type_id, payload = metadata
    if type_id == 4:
        return version_id, payload
    subversions, subscores = zip(*[compute_scores(subpacket) for subpacket in payload])
    version_total = version_id + sum(subversions)
    if type_id == 0:
        score = sum(subscores)
    elif type_id == 1:
        score = prod(subscores)
    elif type_id == 2:
        score = min(subscores)
    elif type_id == 3:
        score = max(subscores)
    elif type_id == 5:
        score = subscores[0] > subscores[1]
    elif type_id == 6:
        score = subscores[0] < subscores[1]
    elif type_id == 7:
        score = subscores[0] == subscores[1]
    return version_total, int(score)


if __name__ == "__main__":
    testinp = open('day16.testinp').read()
    print(*day16(testinp))
    inp = open('day16.inp').read()
    print(*day16(inp))
