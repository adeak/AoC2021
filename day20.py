import numpy as np

def day20(inp):
    it = iter(inp.splitlines())
    algo = np.array(list(next(it))) == '#'
    next(it)
    img = np.array([list(row) for row in it]) == '#'

    # pad with a layer of zeros to get initial padding right
    img = np.pad(img, 1, constant_values=False)

    for i in range(1, 51):
        # pad with background if necessary
        img = pad_image(img)

        # convert 3x3 moving window to corresponding binary
        windowed_shape = np.array(img.shape) - 2
        windowed = np.lib.stride_tricks.sliding_window_view(img, (3, 3)).reshape(*windowed_shape, -1)
        indices = (windowed * 2**np.arange(8, -1, -1)).sum(-1)
        img = algo[indices]

        if i == 2:
            part1 = img.sum()

    part2 = img.sum()

    return part1, part2


def pad_image(img):
    """Ensure there are at least three "dark" or "light" layers around the image."""
    # input image has at least one layer of remaining padding of the current background
    edge_type = img[0, 0]

    pad_width = 3  # at worst
    prev_count = (img != edge_type).sum()
    for peel_depth in range(1, 4):
        current_count = (img[peel_depth:-peel_depth, peel_depth:-peel_depth] != edge_type).sum()
        n_border = prev_count - current_count
        if n_border == 0:
            # there are no non-boundary states on the current edge shell
            pad_width -= 1
        else:
            # there's a bad one; pre-existing border ends here (if any)
            break
        prev_img = current_count

    return np.pad(img, pad_width, constant_values=edge_type)


if __name__ == "__main__":
    testinp = open('day20.testinp').read()
    print(*day20(testinp))
    inp = open('day20.inp').read()
    print(*day20(inp))
