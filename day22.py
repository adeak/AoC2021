from itertools import cycle, count, islice, product
from collections import Counter, defaultdict
import re

import numpy as np

def day22(inp):
    part1 = part2 = None

    all_coords = []
    all_states = []
    for row in inp.splitlines():
        state, rest = row.split()
        coords = [
            sorted(map(int, axis.split('..')))
            for axis in re.sub('[xyz]=', '', rest).split(',')
        ]
        state = state == 'on'

        all_coords.append(coords)
        all_states.append(state)

    all_coords = np.array(all_coords)  # shape (nrules, 3, 2)
    all_states = np.array(all_states)  # shape (nrules,)

    outliers = (all_coords < -50).any((-2, -1)) | (all_coords > 50).any((-2, -1))
    outlier_coords = all_coords[outliers, ...]
    outlier_states = all_states[outliers]
    inner_coords = all_coords[~outliers, ...]
    inner_states = all_states[~outliers]

    minima = inner_coords[..., 0].min(0) # shape (3,)
    maxima = inner_coords[..., 1].max(0) # shape (3,)
    sizes = (maxima - minima) + 1  # shape (3,)

    voxels = np.zeros(shape=sizes, dtype=bool)
    for state, bounds in zip(inner_states, inner_coords):
        ranges = tuple(
            slice(ifrom - minnow, ito - minnow + 1)
            for (ifrom, ito), minnow in zip(bounds, minima)
        )
        voxels[ranges] = state
    part1 = voxels.sum()

    # assume that outliers only overlap a pair at a time...
    on_count = 0 if not outlier_states[0] else outlier_coords[0, ...].ptp(-1).prod()
    for this_ind in range(1, outlier_states.size):
        this_bounds = outlier_coords[this_ind, ...]
        this_state = outlier_states[this_ind]
        overlap_count = 0
        for that_ind in range(this_ind - 1, -1, -1):
            that_state = outlier_states[that_ind]

            # check if there's overlap
            that_bounds = outlier_coords[that_ind, ...]
            overlap_sizes = [
                min(x2, y2) - max(x1, y1) + 1
                for (x1, x2), (y1, y2) in zip(this_bounds, that_bounds)
            ]
            has_overlap = all(overlap_size > 0 for overlap_size in overlap_sizes)
            if not has_overlap:
                continue

            # else: overlap might still be a no-op
            if that_state != this_state:
                # then we're flipping the overlap anyway
                continue

            # else: we're not changing voxels in the overlap
            overlap_count += np.prod(overlap_sizes)

        # flip the state of this region minus overlap_count
        on_count += (this_bounds[:, 1] - this_bounds[:, 0] + 1).prod() - overlap_count
    part2 = part1 + on_count

    return part1, part2



if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    print(*day22(testinp))
    inp = open('day22.inp').read()
    print(*day22(inp))
