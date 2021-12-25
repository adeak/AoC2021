from itertools import product
import re

import numpy as np


def day22(inp, part2=False):
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

    if not part2:
        relevant_states = inner_states
        relevant_coords = inner_coords
    else:
        relevant_states = all_states
        relevant_coords = all_coords

    boxes = set()  # bounds for disjoint boxes that should be turned on at the end
    for state, bounds in zip(relevant_states, relevant_coords):
        bounds = tuple(map(tuple, bounds))
        to_add = {bounds}
        while to_add:
            # find a new (sub)box to add to the "known disjoint" ones
            add_now = to_add.pop()
            # loop over each "known disjoint" lit box and find overlaps
            # once we find an overlap, blow up old and new boxes and start over
            next_boxes = set()
            while boxes:
                other_box = boxes.pop()
                # other_box is known disjoint lit among boxes
                has_overlap = all(
                    x1 <= y1 <= x2
                        or x1 <= y2 <= x2
                        or y1 <= x1 <= x2 <= y2
                    for (x1, x2), (y1, y2) in zip(add_now, other_box)
                )
                if not has_overlap:
                    # nothing to do for now, grab the next known disjoint lit box, if any
                    next_boxes.add(other_box)
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

                if state:
                    next_boxes.add(other_box)

                for subbox in product(*split_coords):
                    # we're generating 27 potential subboxes
                    # but we only have at most 15(?) actual subboxes... so filter these out

                    # also skip degenerate boxes, if any
                    if any(x1 > x2 for x1, x2 in subbox):
                        continue

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
                        x1 < y1 <= x2 < y2 or y1 < x1 <= y2 < x2 or y1 < x1 <= x2 < y2
                        for (x1, x2), (y1, y2) in zip(other_box, subbox)
                    )
                    assert not any(
                        x1 < y1 <= x2 < y2 or y1 < x1 <= y2 < x2 or y1 < x1 <= x2 < y2
                        for (x1, x2), (y1, y2) in zip(add_now, subbox)
                    )

                    if part_of_new and not part_of_old:
                        # need to go another round to check the new pieces
                        to_add.add(subbox)

                    if state:
                        # leave old pieces alone, add "only new" pieces to todo list
                        # (already done before this loop)
                        pass
                    else:
                        # keep all "only old" pieces, and keep track of "off" "only new" ones (already done)
                        if part_of_old and not part_of_new:
                            next_boxes.add(subbox)
                
                # keep remaining, unchecked boxes for next iteration
                next_boxes |= boxes
                break
            else:
                # there was no overlap with any of the known disjoint lit boxes
                # add this box if it's lit
                if state:
                    next_boxes.add(add_now)
                # otherwise this was a no-op box
            boxes = next_boxes
    # now everything in `boxes` are disjoint lit boxes, compute the volume
    boxes = np.array(list(boxes))
    res = (boxes[..., 1] - boxes[..., 0] + 1).prod(-1).sum()

    return res


if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    print(day22(testinp), day22(testinp, part2=True))
    inp = open('day22.inp').read()
    print(day22(inp), day22(inp, part2=True))
