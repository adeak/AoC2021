def day02(inp, part2=False):
    rows = inp.strip().splitlines()

    x = h = aim = 0
    for row in rows:
        dir, val = row.split()
        val = int(val)
        if dir == 'forward':
            x += val
            if part2:
                h += val * aim
            continue
        elif dir == 'up':
            delta = -val
        elif dir == 'down':
            delta = val
        else:
            raise ValueError(f'Invalid direction {dir}.')

        if part2:
            aim += delta
        else:
            h += delta

    return h * x


if __name__ == "__main__":
    inp = open('day02.inp').read()
    print(day02(inp), day02(inp, part2=True))
