import numpy as np

def day01(inp):
    nums = np.fromstring(inp, sep=' ').astype(int)

    part1 = (np.diff(nums) > 0).sum()

    part2 = (np.diff(np.lib.stride_tricks.sliding_window_view(nums, 3).sum(-1)) > 0).sum()

    return part1, part2


if __name__ == "__main__":
    inp = open('day01.inp').read()
    print(day01(inp))
