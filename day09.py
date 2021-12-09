import numpy as np
import scipy.ndimage as ndi

def day09(inp):
    nums = np.array([[int(c) for c in row] for row in inp.strip().splitlines()])

    padded = np.full_like(nums, shape=np.array(nums.shape)+2, fill_value=nums.max()+1)
    padded[1:-1, 1:-1] = nums

    windowed = np.lib.stride_tricks.sliding_window_view(padded, (3, 3))
    windowed_aux = windowed.copy()
    windowed_aux[..., 1, 1] = nums.max() + 1
    minima = (windowed[..., 1:2, 1:2] < windowed_aux).all((-2, -1))

    part1 = (nums[minima] + 1).sum()

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
