from itertools import product
import re

import numpy as np

def day22(inp):
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

    on_count = part1
    boxes = []  # bounds for disjoint boxes that should be turned on
    for state, bounds in zip(outlier_states, outlier_coords):
        bounds = tuple(map(tuple, bounds))
        to_add = {bounds}
        while to_add:
            # find a new (sub)box to add to the "known disjoint" ones
            add_now = to_add.pop()
            # loop over each "known disjoint" lit box and find overlaps
            next_boxes = []
            for other_box in boxes:
                # other_box is known disjoint lit among boxes
                has_overlap = all(
                    x1 <= y1 <= x2
                        or x1 <= y2 <= x2
                        or y1 <= x1 <= x2 <= y2
                    for (x1, x2), (y1, y2) in zip(add_now, other_box)
                )
                if not has_overlap:
                    # nothing to do for now, grab the next known disjoint lit box, if any
                    next_boxes.append(other_box)
                    continue

                # otherwise we must split add_now and maybe other_box into subboxes
                # to cover all possible overlap cases, handle indices on an equal footing
                sorted_coords = [
                    sorted(x1x2 + y1y2)
                    for x1x2, y1y2 in zip(add_now, other_box)
                ]
                split_coords = [
                    (
                        (z1, z2 - 1), # lower non-overlapping section
                        (z2, z3),  # overlapping section
                        (z3 + 1, z4),  # upper overlapping section
                    )
                    for z1, z2, z3, z4 in sorted_coords
                ]

                # if state is on, we already have the overlap turned on
                #    so we only have to add the remaining subboxes of add_now to the todo list
                #    and add back the unsplit other_box to the boxes
                # if state is off, we have to add back the non-overlapping old bits
                # to next_boxes, and non-overlapping bits of add_now to the todo list

                for subbox in product(*split_coords):
                    # we're generating 27 potential subboxes
                    # but we only have at most 15(?) actual subboxes... so filter these out

                    # check if this subbox is part of the old big one and the new big one
                    part_of_old = all(
                        x1 <= y1 <= y2 <= x2
                        for (x1, x2), (y1, y2) in zip(other_box, subbox)
                    )
                    part_of_new = all(
                        x1 <= y1 <= y2 <= x2
                        for (x1, x2), (y1, y2) in zip(add_now, subbox)
                    )
                    assert not any(
                        x1 < y1 <= x2 < y2 or y1 < x1 <= y2 < x2
                        for (x1, x2), (y1, y2) in zip(other_box, subbox)
                    )
                    assert not any(
                        x1 < y1 <= x2 < y2 or y1 < x1 <= y2 < x2
                        for (x1, x2), (y1, y2) in zip(add_now, subbox)
                    )
                    if part_of_old and not part_of_new:
                        # this part was lit and we're not turning it off
                        # because it doesn't overlap; keep it
                        next_boxes.append(subbox)
                    elif part_of_old and state:
                        # this part was lit, and it overlaps with "on" new block
                        # but we're going to remove it and let it be replaced with
                        # this new block after the end of this big loop...
                        pass
                    if part_of_new:
                        # always keep each new bit until there's no overlap with anything
                        to_add.add(subbox)
                break
            else:
                # there was no overlap with any of the known disjoint lit boxes
                # add this box if it's lit
                if state:
                    next_boxes.append(add_now)
                # otherwise this was a no-op
            boxes = next_boxes

    # now everything in `boxes` are disjoint lit boxes
    assert all(bound[0] < bound[1] for bounds in boxes for bound in bounds)
    assert all(
        not all(
            x1 <= y1 <= x2 or x1 <= y2 <= x2
            for (x1, x2), (y1, y2) in zip(box, box2)
        )
        for i, box in enumerate(boxes)
        for box2 in boxes[i+1:]
    )
    boxes = np.array(boxes)
    part2 = on_count + (boxes[..., 1] - boxes[..., 0] + 1).prod(-1).sum()

    return part1, part2



if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    testinp2 = open('day22.testinp2').read()
    print(*day22(testinp2))
    inp = open('day22.inp').read()
    print(*day22(inp))
