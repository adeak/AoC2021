from collections import Counter
from operator import itemgetter

def day14(inp):
    part1 = part2 = None
    it = iter(inp.splitlines())

    template = next(it)
    next(it)
    rules = dict(row.split(' -> ') for row in it)

    polymer = template
    for i in range(10):
        next_poly = [polymer[0]]
        pairs = (polymer[ind:ind+2] for ind in range(len(polymer) - 1))
        for pair in pairs:
            infix = rules.get(pair, '')
            next_poly.append(infix + pair[1])
        polymer = ''.join(next_poly)

    counts = Counter(polymer)
    ranked = sorted(counts.values())
    part1 = ranked[-1] - ranked[0]

    return part1, part2


if __name__ == "__main__":
    testinp = open('day14.testinp').read()
    print(*day14(testinp))
    inp = open('day14.inp').read()
    print(*day14(inp))
