from itertools import count
import numpy as np

def day11(inp):
    levels = np.ma.array([[int(c) for c in row] for row in inp.splitlines()])

    flashes = 0
    for step in count(1):
        levels += 1
        flash_octopodes(levels)

        # masked values are the ones who flashed
        flash_contrib = levels.mask.sum()
        levels[levels.mask] = 0  # also resets the mask

        if step == 100:
            flashes += flash_contrib
        if flash_contrib == levels.size:
            sync_iter = step
            break

    part1 = flashes
    part2 = sync_iter

    return part1, part2


def flash_octopodes(levels):
    """Recursively flash the octopodes until all are done.

    Octopodes are stored in a masked array, octopodes that
    have flashed are masked out. The function mutates the
    input, so in the end we can harvest the mask.

    """
    flashers = levels > 9
    num_flashers = flashers.sum()
    if not num_flashers:
        # we're done
        return
    # otherwise mask out new flashers
    levels.mask |= flashers

    # generate exact 2d indices for incrementing, in order
    # to be able to sum up contributions from adjacent sites
    i, j = flashers.nonzero()  # flasher indices
    i_neighbs = i[:, None] + [-1, -1, -1, 0, 0, 1, 1, 1]
    j_neighbs = j[:, None] + [-1, 0, 1, -1, 1, -1, 0, 1]
    # discard out-of-bounds indices (cost of not padding)
    keep_inds = ((i_neighbs < levels.shape[0]) & (i_neighbs >= 0)
                &(j_neighbs < levels.shape[1]) & (j_neighbs >= 0))
    np.add.at(levels, (i_neighbs[keep_inds], j_neighbs[keep_inds]), 1)

    # find next link in the cascade
    flash_octopodes(levels)


if __name__ == "__main__":
    testinp = open('day11.testinp').read()
    print(*day11(testinp))
    inp = open('day11.inp').read()
    print(*day11(inp))
