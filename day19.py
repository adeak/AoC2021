from collections import Counter, defaultdict

import numpy as np
from scipy.spatial.distance import pdist

def day19(inp):
    it = iter(inp.splitlines())
    scanner_data = []
    for row in it:
        if row.startswith('---'):
            this_scanner = []
            continue
        if not row.strip():
            scanner_data.append(np.array(this_scanner))
            continue
        this_scanner.append(list(map(int, row.split(','))))
    scanner_data.append(np.array(this_scanner))

    # get pairwise distances
    dists = [pdist(coords, metric='cityblock') for coords in scanner_data]

    # get overlapping distances
    overlaps = np.array([
        [
            # watch out for multiplicities
            sum((Counter(i) & Counter(j)).values())
            for j in dists
        ]
        for i in dists
    ])
    # filter out diagonal
    np.einsum('ii->i', overlaps)[:] = 0  # writeable view
    # filter out where less than 12*11/2 == 66
    overlaps[overlaps < 12*11/2] = 0
    # find overlapping indices in the upper triangle
    i, j = overlaps.nonzero()
    overlap_mapping = defaultdict(set)
    for ival, jval in zip(i, j):
        overlap_mapping[ival].add(jval)

    # overlap_mapping specifies a graph, but that's not too important
    # start from an edge, find an uncharted neighbour, fit their coordinates

    n_scanners = len(overlap_mapping)
    current = 0
    mapped = {current}
    exhausted = set()
    unmapped = set(range(1, n_scanners))
    mapping_order = []
    while unmapped:
        # find next edge to map out
        candidates = overlap_mapping[current] - (mapped | exhausted)
        if not candidates:
            # we've run out of neighbours for `current`
            del overlap_mapping[current]
            exhausted.add(current)
            mapped.remove(current)
            current = next(iter(mapped))
            continue
        neighbour = candidates.pop()
        mapped.add(neighbour)
        unmapped.remove(neighbour)
        mapping_order.append((current, neighbour))

    # now we just go pair by pair and match the overlaps...
    origin = mapping_order[0][0]
    origins = {origin: np.array([0, 0, 0])}
    beacon_positions = set(map(tuple, scanner_data[origin]))
    for reference, other in mapping_order:
        origin_shift = transform_other_positions(scanner_data, dists, reference, other)
        origins[other] = origins[reference] + origin_shift
        beacon_positions |= set(map(tuple, scanner_data[other] + origins[other]))

    part1 = len(beacon_positions)
    part2 = pdist(list(origins.values()), metric='cityblock').max().astype(int)

    return part1, part2


def transform_other_positions(scanner_data, dists, ref, other):
    ref_poses = scanner_data[ref]
    other_poses = scanner_data[other]
    ref_dists = dists[ref]
    other_dists = dists[other]

    # reduce positions to those that might overlap
    # by selecting those that are involved in matching distances
    matching_dists = np.intersect1d(ref_dists, other_dists)
    aux_poses = []
    for poses, dists in zip([ref_poses, other_poses], [ref_dists, other_dists]):
        n = poses.shape[0]
        matches = np.isin(dists, matching_dists)
        inds_keep = np.array(np.triu(np.ones((n, n)), 1).nonzero())[:, matches]
        inds_keep = np.intersect1d(*inds_keep)
        aux_poses.append(poses[inds_keep, :])
    ref_poses, other_poses = aux_poses

    most_overlaps = 0
    for order in [0, 1, 2], [1, 2, 0], [2, 0, 1], [0, 2, 1], [2, 1, 0], [1, 0, 2]:
        improper_order = (order < np.roll(order, 1)).sum() > 1
        for sign_flip_trio in np.reshape(np.meshgrid(*[(-1, 1)]*3), (3, -1)).T:
            improper_flip = sign_flip_trio.prod() == -1
            if improper_order ^ improper_flip:
                # improper rotation
                continue

            candidate_poses = other_poses[:, order] * sign_flip_trio
            for ref_pos in ref_poses:
                for other_pos in candidate_poses:
                    shifteds = candidate_poses + (ref_pos - other_pos)
                    overlaps = len(set(map(tuple, ref_poses)) & set(map(tuple, shifteds)))
                    if overlaps > most_overlaps:
                        most_overlaps = overlaps
                        origin_shift = ref_pos - other_pos
                        best_candidate_poses = scanner_data[other][:, order] * sign_flip_trio
    scanner_data[other][...] = best_candidate_poses

    return origin_shift


if __name__ == "__main__":
    testinp = open('day19.testinp').read()
    print(*day19(testinp))
    inp = open('day19.inp').read()
    print(*day19(inp))
