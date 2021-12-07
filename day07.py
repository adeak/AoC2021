import numpy as np

def day07(inp):
    nums = map(int, inp.strip().split(','))
    poses = np.fromstring(inp, sep=',', dtype=int)

    steps = abs(poses - np.arange(poses.size)[:, None])  # this only works by accident
    part1 = steps.sum(-1).min()
    part2 = (steps*(steps + 1)/2).sum(-1).min().astype(int)

    return part1, part2


if __name__ == "__main__":
    testinp = open('day07.testinp').read()
    print(*day07(testinp))
    inp = open('day07.inp').read()
    print(*day07(inp))
