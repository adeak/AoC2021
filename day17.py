from itertools import count
import numpy as np

def day17(inp):
    xpart, ypart = inp.split()[-2:]
    xfrom, xto = sorted(map(int, xpart[2:-1].split('..')))
    yfrom, yto = sorted(map(int, ypart[2:].split('..')))

    # if target is negative, switch to positive and always use positive vx
    if xfrom < 0:
        xfrom, xto = -xto, -xfrom
    assert xto > 0

    # brute force for now...
    # negative initial vy values necessary for part 2
    # max y velocity: it will have same speed coming down at x == 0...
    #     so it mustn't miss the bottom of the box in the next step
    # and it's not worth bothering with a better lower x limit
    assert yto < 0
    vxs, vys = np.mgrid[1:xto + 1, yfrom:abs(yfrom) + 1]
    poses_x = np.zeros_like(vxs)
    poses_y = np.zeros_like(vys)
    max_heights = np.zeros_like(poses_x)
    hits = np.zeros_like(poses_y, dtype=bool)
    misses = np.zeros_like(poses_y, dtype=bool)

    for it in count(1):
        # update position
        poses_x += vxs
        poses_y += vys

        # update speeds
        vxs -= 1
        vxs[vxs < 0] = 0
        vys -= 1

        # check for max
        new_record = poses_y > max_heights
        max_heights[new_record] = poses_y[new_record]

        # check for target and miss
        hits |= (xfrom <= poses_x) & (poses_x <= xto) & (yfrom <= poses_y) & (poses_y <= yto)
        misses |= (poses_y < yfrom) & ~hits

        # check if we need to keep working
        if (hits | misses).sum() == poses_y.size:
            break

    part1 = max_heights[hits].max()
    part2 = hits.sum()

    return part1, part2


if __name__ == "__main__":
    testinp = open('day17.testinp').read()
    print(*day17(testinp))
    inp = open('day17.inp').read()
    print(*day17(inp))
