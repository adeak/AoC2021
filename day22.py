from itertools import product
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

    on_count = part1
    boxes = []  # bounds for boxes that should be turned on
    for state, bounds in zip(outlier_states, outlier_coords):
        bounds = tuple(map(tuple, bounds))
        to_add = {bounds}
        while to_add:
            # find a new (sub)box to add to the "known disjoint" ones
            add_now = to_add.pop()
            #print(f'trying to add {add_now} {state}...')
            # loop over each "known disjoint" lit box and find overlaps
            next_boxes = []
            for other_box in boxes:
                #print(f'comparing with {other_box}...')
                # other_box is known disjoint lit among boxes
                has_overlap = all(
                    x1 <= y1 <= x2 or x1 <= y2 <= x2
                    for (x1, x2), (y1, y2) in zip(add_now, other_box)
                )
                if not has_overlap:
                    #print('no overlap...')
                    # nothing to do for now
                    next_boxes.append(other_box)
                    continue
                # make sure that boxes don't engulf each other
                assert all(
                    x1 <= y1 <= x2 <= y2 or y1 <= x1 <= y2 <= x2
                    for (x1, x2), (y1, y2) in zip(add_now, other_box)
                ), (add_now, other_box)
                # otherwise we must split add_now and maybe other_box into subboxes
                split_coords = [
                    (
                        (min(x1, y1), max(x1, y1) - 1),  # lower non-overlapping section
                        (max(x1, y1), min(x2, y2)),      # overlapping section
                        (min(x2, y2) + 1, max(x2, y2)),  # upper overlapping section
                    )
                    for (x1, x2), (y1, y2) in zip(add_now, other_box)
                ]
                # sections = [
                #     (
                #         max(x1, y1) - min(x1, y1),  # lower non-overlapping size
                #         min(x2, y2) - max(x1, y1) + 1,  # overlapping size
                #         max(x2, y2) - min(x2, y2),  # upper non-overlapping size
                #     for (x1, x2), (y1, y2) in zip(bounds, other_box):
                # ]

                # if state is on, we already have the overlap turned on
                #    so we only have to add the remaining subboxes of add_now to the todo list
                #    and add back the unsplit other_box to the boxes
                # if state is off, we have to add back the non-overlapping old bits
                # to next_boxes, and non-overlapping bits of add_now to the todo list

                if state:
                    # the "other" box is left invariant, no need to harm it
                    # just add non-overlapping new bits later
                    next_boxes.append(other_box)

                for ijk in product(range(3), repeat=3):
                    # we're generating 27 potential subboxes
                    # but we only have at most 15 actual subboxes... so filter these out
                    subbox = tuple(
                        split_coord[index]
                        for index, split_coord in zip(ijk, split_coords)
                    )

                    if ijk == (1, 1, 1):
                        # this is the overlapping box
                        if not state:
                            # turn or leave it off
                            # don't add the overlap back
                            continue
                        # else keep the lit overlapping box
                        next_boxes.append(subbox)
                    else:
                        # always add non-overlapping new bits
                        part_of_new = all(
                            x1 <= y1 <= y2 <= x2
                            for (x1, x2), (y1, y2) in zip(add_now, subbox)
                        )
                        part_of_old = all(
                            x1 <= y1 <= y2 <= x2
                            for (x1, x2), (y1, y2) in zip(other_box, subbox)
                        )
                        if part_of_new:
                            to_add.add(subbox)
                        elif part_of_old:
                            # non-overlapping old lit part; only add if we're turning off
                            if not state:
                                next_boxes.append(subbox)
                break
            else:
                # there was no overlap with any of the known disjoint lit boxes
                # add this box if it's lit
                if state:
                    next_boxes.append(add_now)
            boxes = next_boxes

    # now everything in `boxes` is a disjoint lit box
    assert all(bound[0] < bound[1] for bounds in boxes for bound in bounds)
    part2 = on_count + sum(
        np.prod([
            x2 - x1 + 1
            for x1, x2 in box
        ])
        for box in boxes
    )

    return part1, part2



if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    testinp2 = open('day22.testinp2').read()
    print(day22(testinp)[0], day22(testinp2)[1])
    inp = open('day22.inp').read()
    print(*day22(inp))
