import numpy as np

def day15(inp, part2=False):
    dat = np.array([[int(c) for c in row] for row in inp.splitlines()])

    if part2:
        offsets = np.indices((5, 5)).sum(0)  # shape (5, 5) increments
        m, n = dat.shape
        # broadcast in 4d and reshape back to 2d
        dat = (dat[..., None, None] + offsets).transpose(2, 0, 3, 1).reshape(m*5, n*5)
        # wrap values back to [1, 9]
        dat = (dat - 1) % 9 + 1

    costs = np.full_like(dat, fill_value=dat.sum())
    costs[0, 0] = 0
    edges = {(0, 0)}
    end = tuple(np.array(dat.shape) - 1)
    while edges:
        next_edges = set()
        for edge in edges:
            cost_now = costs[edge]
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighb = edge[0] + di, edge[1] + dj
                if not (0 <= neighb[0] < dat.shape[0] and 0 <= neighb[1] < dat.shape[1]):
                    # invalid position
                    continue
                cost_neighb = cost_now + dat[neighb]
                if cost_neighb > costs[neighb]:
                    # we already had a better path here, stop
                    continue
                # else this is the best path here so far
                costs[neighb] = cost_neighb
                # continue from here unless we're done with this path
                if neighb != end:
                    next_edges.add(neighb)
        edges = next_edges
    res = costs[end]

    return res


if __name__ == "__main__":
    testinp = open('day15.testinp').read()
    print(day15(testinp), day15(testinp, part2=True))
    inp = open('day15.inp').read()
    print(day15(inp), day15(inp, part2=True))
