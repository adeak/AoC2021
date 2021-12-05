import numpy as np

def day05(inp):
    rows = inp.strip().splitlines()
    froms = []
    tos = []
    for row in rows:
        fromstr, tostr = row.split(' -> ')
        froms.append(np.fromstring(fromstr, sep=',', dtype=int))
        tos.append(np.fromstring(tostr, sep=',', dtype=int))
    froms = np.array(froms)
    tos = np.array(tos)

    # assume non-negative indices, don't bother with optimising lower bound
    size = np.vstack([froms, tos]).max(0) + 1
    board = np.zeros(size, dtype=int)

    linecounts = board.copy()
    i_inds = []
    j_inds = []
    i_inds_part2 = []
    j_inds_part2 = []
    for i in range(froms.shape[0]):
        # generate index arrays where ones should be added
        fromnow, tonow = froms[i], tos[i]
        deltas = tonow - fromnow
        n_points = abs(deltas).max() + 1
        ivals = np.linspace(fromnow[0], tonow[0], n_points, dtype=int)
        jvals = np.linspace(fromnow[1], tonow[1], n_points, dtype=int)

        # special-case part 2 (diagonal lines)
        if abs(deltas).min() == 0:
            targets = i_inds, j_inds
        else:
            targets = i_inds_part2, j_inds_part2

        targets[0].extend(ivals)  # contains indices along first axis
        targets[1].extend(jvals)  # contains indices along second axis

    # add 1 to every index
    np.add.at(linecounts, (i_inds, j_inds), 1)
    part1 = (linecounts >= 2).sum()

    # add part 2 contribution separately
    np.add.at(linecounts, (i_inds_part2, j_inds_part2), 1)
    part2 = (linecounts >= 2).sum()

    return part1, part2


if __name__ == "__main__":
    testinp = open('day05.testinp').read()
    print(*day05(testinp))
    inp = open('day05.inp').read()
    print(*day05(inp))
