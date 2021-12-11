from itertools import count
import numpy as np

def day11(inp):
    dat = np.ma.array([[int(c) for c in row] for row in inp.splitlines()])

    flashes = 0
    for i in count(1):
        dat += 1
        flash_octopodes(dat)
        flash_contrib = dat.mask.sum()
        dat[dat.mask] = 0
        dat.mask = False

        if i == 100:
            flashes += flash_contrib
        if flash_contrib == dat.size:
            sync_iter = i
            break

    part1 = flashes
    part2 = sync_iter

    return part1, part2


def flash_octopodes(dat):
    flashers = dat > 9
    num_flashers = flashers.sum()
    if not num_flashers:
        return
    dat.mask |= flashers

    i, j = flashers.nonzero()  # flasher indices
    i_neighbs = i[:, None] + [-1, -1, -1, 0, 0, 1, 1, 1]
    j_neighbs = j[:, None] + [-1, 0, 1, -1, 1, -1, 0, 1]
    keep_inds = ((i_neighbs < dat.shape[0]) & (i_neighbs >= 0)
                &(j_neighbs < dat.shape[1]) & (j_neighbs >= 0))
    np.add.at(dat, (i_neighbs[keep_inds], j_neighbs[keep_inds]), 1)
    flash_octopodes(dat)


if __name__ == "__main__":
    testinp = open('day11.testinp').read()
    print(*day11(testinp))
    inp = open('day11.inp').read()
    print(*day11(inp))
