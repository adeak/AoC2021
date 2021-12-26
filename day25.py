from itertools import count

import numpy as np


def day25(inp):
    floor = np.array([list(row) for row in inp.splitlines()])
    shape = floor.shape

    kind_codes = '>v'
    deltas = np.array([(0, 1), (1, 0)])
    poses = [np.array((floor == kind_code).nonzero()) for kind_code in kind_codes]
    # two lists with shape (2, n1) and (2, n2) for the two herds:
    # for each herd and each axis n_specimens indices

    # convert 2d indices to linear indices for faster lookup later
    poses = [np.ravel_multi_index(poses_now, shape) for poses_now in poses]

    n_east = poses[0].size
    all_poses = np.concatenate(poses)
    poses = all_poses[:n_east], all_poses[n_east:]
    # now both elements of poses are a view into the same underlying array

    for i in count(1):
        could_move = False
        for kind, delta in enumerate(deltas):
            poses_now = poses[kind]
            cucumbs = np.unravel_index(poses_now, shape)  # shape (n_herd, 2) proper 2d indices
            next_poses = np.ravel_multi_index(cucumbs + delta[:, None], shape, mode='wrap')  # shape (n_herd,) 1d indices

            # find free cucumbers
            free_poses_mask = ~np.in1d(next_poses, all_poses)
            poses_now[free_poses_mask] = next_poses[free_poses_mask]

            if free_poses_mask.any():
                # this herd could move
                could_move = True
        if not could_move:
            # we're done
            return i


if __name__ == "__main__":
    testinp = open('day25.testinp').read()
    print(day25(testinp))
    inp = open('day25.inp').read()
    print(day25(inp))
