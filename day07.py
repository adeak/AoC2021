import numpy as np

def day07(inp):
    nums = map(int, inp.strip().split(','))
    poses = np.fromstring(inp, sep=',', dtype=int)

    diffs = abs(poses - np.arange(poses.size)[:, None]).sum(-1)
    mindiff_pos = diffs.argmin()
    mindiff = diffs[mindiff_pos]
    part1 = mindiff

    steps = abs(poses - np.arange(poses.size)[:, None])
    diffs = ((steps * (steps+1)).sum(-1)/2).astype(int)
    mindiff_pos = diffs.argmin()
    mindiff = diffs[mindiff_pos]
    part2 = mindiff

    return part1, part2


if __name__ == "__main__":
    testinp = open('day07.testinp').read()
    print(*day07(testinp))
    inp = open('day07.inp').read()
    print(*day07(inp))
