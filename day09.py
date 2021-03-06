import numpy as np
import scipy.ndimage as ndi

def day09(inp):
    nums = np.array([[int(c) for c in row] for row in inp.strip().splitlines()])

    # pad (with max) to include edge values
    padded = np.pad(nums, 1, constant_values=nums.max())

    # get 3x3 sliding window to check for minima
    # watch out and only check 4-neighbourhood
    windowed = np.lib.stride_tricks.sliding_window_view(padded, (3, 3))
    minima = (windowed[..., 1, 1, None] < windowed[..., [0, 2, 1, 1], [1, 1, 0, 2]]).all(-1)  # bools with nums.shape
    part1 = (nums[minima] + 1).sum()

    # part 2: flood fill with 9 as boundaries -> turn into a binary image
    img = nums != 9
    labels, num_features = ndi.label(img)
    sizes = ndi.labeled_comprehension(img, labels, range(1, num_features + 1), np.size, int, 0)
    part2 = np.prod(sorted(sizes)[-3:])

    return part1, part2


if __name__ == "__main__":
    testinp = open('day09.testinp').read()
    print(*day09(testinp))
    inp = open('day09.inp').read()
    print(*day09(inp))
