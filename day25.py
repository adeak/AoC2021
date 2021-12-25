from itertools import count
import numpy as np

def day25(inp):
    floor_raw = np.array([list(row) for row in inp.splitlines()])
    shape = floor_raw.shape

    deltas = np.array([(0, 1), (1, 0)])
    encoding = dict(zip('>v', deltas))
    floor = np.full(shape, fill_value=-1)
    for kind, code in enumerate(encoding):
        floor[floor_raw == code] = kind  # 0, 1 for the four kinds (floor is -1 lava)

    # brute force
    for i in count(1):
        could_move = False
        for kind in range(2):
            cuc_mask = floor == kind
            directions = deltas[floor]  # shape (m, n, 2) for each site; only sane where cuc_mask is True
            cuc_inds = np.array(cuc_mask.nonzero()).T  # shape (n_cucs, 2) indices (old positions)
            next_poses = np.mod(cuc_inds + directions[tuple(cuc_inds.T)], shape)  # shape (n_cucs, 2) indices

            # find free cucumbers
            free_poses_mask = floor[next_poses[:, 0], next_poses[:, 1]] == -1
            next_poses = next_poses[free_poses_mask]  # shape (n_mobile, 2) new positions
            cuc_inds = cuc_inds[free_poses_mask]  # shape (n_mobile, 2) old positions

            # step free cucumbers
            floor[tuple(next_poses.T)] = floor[tuple(cuc_inds.T)]
            floor[tuple(cuc_inds.T)] = -1

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
