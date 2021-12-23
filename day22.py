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
    all_items = zip(outlier_coords, outlier_states)
    boxes = np.array([next(all_items)[0]])  # shape (1, 3, 2)
    for box_index, (box_to_add, state) in enumerate(all_items, 1):
        print(f'New box #{box_index} {box_to_add}, {state}...')
        #subboxes_todo = [box_to_add]
        subboxes_todo = {tuple(map(tuple, box_to_add))}
        while subboxes_todo:
            print(len(subboxes_todo))
            # assert not any(
            #     np.array_equal(boxes[i, ...], boxes[j, ...])
            #     for i in range(boxes.shape[0])
            #     for j in range(i + 1, boxes.shape[0])
            # ), boxes
            #print('subboxes:')
            #print(subboxes_todo)
            box_new = np.array(subboxes_todo.pop())
            # bounds is shape (3, 2)
            overlappeds = (
                ((boxes[..., 0] <= box_new[..., 0]) & (box_new[..., 0] <= boxes[..., 1])) |  # x1 <= y1 <= x2
                ((boxes[..., 0] <= box_new[..., 1]) & (box_new[..., 1] <= boxes[..., 1])) |  # x1 <= y2 <= x2
                ((box_new[..., 0] <= boxes[..., 0]) & (boxes[..., 1] <= box_new[..., 1]))    # y1 <= x1 <= x2 <= y2
            ).all(-1)  # shape (n_boxes,) bool
            next_boxes = [boxes[~overlappeds, ...]]  # these need not change

            if not overlappeds.any():
                # there were no overlaps, we're done with this subbox
                #print(f'no overlaps... for {box_new}')
                #print(f'all_boxes: {boxes}')
                if state:
                    next_boxes.append(box_new[None, ...])
                boxes = np.concatenate(next_boxes)
                continue
            #print(f'splitting {box_new}')
            #print('splitting...')

            # split the rest
            overlappers = boxes[overlappeds, ...]  # shape (n_overlapping, 3, 2)
            joined_coords = np.empty(overlappers.shape + (2,), dtype=int)
            joined_coords[..., 0] = overlappers
            joined_coords[..., 1] = box_new
            joined_coords = joined_coords.reshape(*overlappers.shape[:-1], -1)  # shape (n_overlapping, 3, 4) with (x1, y1, x2, y2) or similar along last axis
            sorted_coords = np.sort(joined_coords, axis=-1)  # now last axis is sorted (independently for each box and each axis): (z1, z2, z3, z4)
            splitting_inds = np.array([
                [sorted_coords[..., 0], sorted_coords[..., 1] - 1],  # (z1, z2 - 1) non-overlap
                [sorted_coords[..., 1], sorted_coords[..., 2]],      # (z2, z3)     overlap
                [sorted_coords[..., 2] + 1, sorted_coords[..., 3]],  # (z3 + 1, z4) non-overlap
            ]).transpose(2, 3, 0, 1)  # shape (n_overlapping, 3, 3, 2) == (n_overlapping, n_dimensions, n_splitpairs, points_in_splitpair)
            # WARNING: some of these index pairs are nonsense for degenerate overlaps, filter them out later
            # the (3, 3)-shaped size here defines the 3x3x3 subcubes
            # through the 3 + 3 + 3 split intervals along the 3 axes
            cube_inds = np.indices((3, 3, 3))  # shape (3, 3, 3, 3), 3 index arrays of shape (3, 3, 3) defining the Cartesian product
            cube_inds = cube_inds.reshape(3, -1).T  # shape (27, 3), 27 index triples of the Cartesian product
            #cube_ind = cube_inds[15, :]
            #assert np.array_equal(splitting_inds[:, range(3), cube_inds, :][:, 15, ...], splitting_inds[:, [0, 1, 2], cube_ind, :])
            subbox_inds = splitting_inds[:, range(3), cube_inds, :]  # shape (n_overlapping, 27, 3, 2)
            # this specifies for each known disjoint lit box where the 27 subboxes are located,
            # some of which overlap with the old box, some with the new, and some with neither

            # filter out nonsense (degenerate, empty, etc.) subboxes
            inds_keep = (subbox_inds[..., 0] <= subbox_inds[..., 1]).all(-1)  # shaped (n_overlapping, 27)

            # assert not any(
            #     np.array_equal(subbox_inds[i, ...], subbox_inds[j, ...])
            #     for i in range(subbox_inds.shape[0])
            #     for j in range(i + 1, subbox_inds.shape[0])
            # ), subbox_inds

            #print(overlappers)
            #print(overlappers.shape, subbox_inds.shape)
            #print(subbox_inds[0, :, 0, :])
            #print(sorted_coords[0, ...])

            part_of_old = (
                (overlappers[:, None, :, 0] <= subbox_inds[..., 0]) & (subbox_inds[..., 0] <= overlappers[:, None, :, 1])
                # shape (n_overlapping, 27, 3) == (n_overlapping, n_subboxes, n_dims)
                # whether for the given disjoint lit box and for the given axis the 27 subboxes overlap or not
            ).all(-1) & inds_keep  # shape (n_overlapping, 27) bool telling which subboxes overlap with the corresponding lit subboxes
            part_of_new = (
                (box_new[:, 0] <= subbox_inds[..., 0]) & (subbox_inds[..., 0] <= box_new[:, 1])
            ).all(-1) & inds_keep  # shape (n_overlapping, 27) bool telling which subboxes overlap with the new subbox
            only_new = part_of_new & ~part_of_old
            only_old = part_of_old & ~part_of_new
            #print(part_of_old.sum(-1), part_of_new.sum(-1), only_old.sum(-1))

            # new strategy:
            #    1. if state is "on", leave old pieces alone, and add "only_new" pieces to todo list
            #    2. if state is "off", keep all "only_old" pieces, discard rest (including pieces of new)
            if state:
                #next_boxes = boxes  # keep originals: boxes untouched actually
                s = {tuple(map(tuple, b)) for b in subbox_inds[only_new, ...]}
                subboxes_todo |= s  # add "only new" pieces to todo list
            else:
                next_boxes.extend(subbox_inds[only_old, ...])
                boxes = np.concatenate(next_boxes)
            continue
            # TODO: cut after this part if the above works

            # add parts of the new box to the todo list
            #print(f'to add to todo: {subbox_inds[part_of_new, ...]}')
            #print(f'part of new: {part_of_new.shape}, {part_of_new.sum()}, {subbox_inds[part_of_new, ...].shape}')
            #print(subbox_inds[part_of_new, ...].shape, np.unique(subbox_inds[part_of_new, ...], axis=0).shape)

            #subboxes_todo.extend(subbox_inds[part_of_new, ...])  # (n, 3, 2) unpacked to list of (3, 2)-shaped boxes
            s = {tuple(map(tuple, b)) for b in subbox_inds[part_of_new, ...]}
            subboxes_todo |= s  # (n, 3, 2) unpacked to list of (3, 2)-shaped boxes

            # add parts of the old box that aren't in the new box
            if only_old.any():
                next_boxes.append(subbox_inds[only_old, ...])  # (n', 3, 2) to be concatenated at the end
                #next_boxes.append(np.unique(subbox_inds[only_old, ...], axis=0))  # (n', 3, 2) to be concatenated at the end
                #print(f'adding {subbox_inds[only_old, ...]}...')
            #input()

            # don't add the overlap:
            #     either we're turning it off,
            #     or we're turning it on but that'll happen when the corresponding "new" subbox has no overlap anymore

            boxes = np.concatenate(next_boxes)

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
    part2 = on_count + (boxes[..., 1] - boxes[..., 0] + 1).prod(-1).sum()

    return part1, part2



if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    testinp2 = open('day22.testinp2').read()
    print(*day22(testinp2))
    inp = open('day22.inp').read()
    print(*day22(inp))
