import numpy as np

def day13(inp):
    it = iter(inp.splitlines())
    inds = []
    for row in it:
        if not row.strip():
            break
        inds.append(list(map(int, row.split(','))))
    inds = np.array(inds)  # shape (ndots, 2)

    # keep the array oriented the same as the input example
    # (i.e. x and y are reversed)
    shape = (inds.max(0) + 1)[::-1]
    sheet = np.zeros(shape=shape, dtype=bool)
    sheet[inds[:, 1], inds[:, 0]] = True

    for i, row in enumerate(it, 1):
        info = row.split()[-1]
        dir, center = info.split('=')
        center = int(center)

        if dir == 'x':
            # just work on the transpose
            sheet = sheet.T

        assert not sheet[center, :].any()
        len_top = center
        len_bottom = sheet.shape[0] - center - 1
        foldlen = min([len_top, len_bottom])
        slice_top = sheet[center - foldlen : center, :]
        slice_bottom = sheet[center + 1 : center + foldlen + 1, :]
        if len_bottom < len_top:
            # keep the "top" part
            slice_top[...] |= slice_bottom[::-1, :]
            sheet = sheet[:center, :]
        else:
            # keep the "bottom" part
            slice_bottom[...] |= slice_top[::-1, :]
            sheet = sheet[:center:-1, :]  # keep "up" up

        if dir == 'x':
            # transpose back for next fold
            sheet = sheet.T

        if i == 1:
            part1 = sheet.sum()

    # part 2
    print('\n'.join(''.join('*' if c else ' ' for c in row) for row in sheet.repeat(2, axis=1)))

    return part1


if __name__ == "__main__":
    testinp = open('day13.testinp').read()
    print(day13(testinp))
    inp = open('day13.inp').read()
    print(day13(inp))
