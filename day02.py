def day02(inp):
    rows = inp.strip().splitlines()

    x = h = 0
    for row in rows:
        dir, val = row.split()
        val = int(val)
        if dir == 'forward':
            x += val
        elif dir == 'up':
            h -= val
        elif dir == 'down':
            h += val
        else:
            assert False
    part1 =  h * x

    x = h = aim = 0
    for row in rows:
        dir, val = row.split()
        val = int(val)
        if dir == 'forward':
            x += val
            h += val * aim
        elif dir == 'up':
            aim -= val
        elif dir == 'down':
            aim += val
        else:
            assert False
    part2 = x * h

    return part1, part2


if __name__ == "__main__":
    inp = open('day02.inp').read()
    print(*day02(inp))
