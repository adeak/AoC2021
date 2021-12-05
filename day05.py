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
        fromnow, tonow = froms[i], tos[i]
        if froms[i][0] == tos[i][0]:
            inds = fromnow[1], tonow[1]
            jvals = np.arange(min(inds), max(inds) + 1)
            ivals = np.full_like(jvals, fill_value=fromnow[0])
        elif froms[i][1] == tos[i][1]:
            inds = fromnow[0], tonow[0]
            ivals = np.arange(min(inds), max(inds) + 1)
            jvals = np.full_like(ivals, fill_value=fromnow[1])
        else:
            # part 2
            n_points = abs(tonow[0] - fromnow[0]) + 1
            ivals = np.linspace(fromnow[0], tonow[0], n_points, dtype=int)
            jvals = np.linspace(fromnow[1], tonow[1], n_points, dtype=int)
            i_inds_part2.extend(ivals)
            j_inds_part2.extend(jvals)
            continue

        i_inds.extend(ivals)
        j_inds.extend(jvals)

    np.add.at(linecounts, (i_inds, j_inds), 1)
    part1 = (linecounts >= 2).sum()

    np.add.at(linecounts, (i_inds_part2, j_inds_part2), 1)
    part2 = (linecounts >= 2).sum()

    return part1, part2


if __name__ == "__main__":
    testinp = open('day05.testinp').read()
    print(*day05(testinp))
    inp = open('day05.inp').read()
    print(*day05(inp))
