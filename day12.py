from collections import defaultdict, Counter

def day12(inp, part2=False):
    conn_aux = [row.split('-') for row in inp.splitlines()]
    conn = defaultdict(set)
    for src, dest in conn_aux:
        # watch out for non-directed edges
        conn[src].add(dest)
        conn[dest].add(src)

    paths = {('start',)}
    complete_paths = set()
    while True:
        next_paths = set()
        for path in paths:
            for next_edge in conn[path[-1]]:
                # no-brainers: ignore start and collect on end
                if next_edge == 'start':
                    continue
                if next_edge == 'end':
                    complete_paths.add(path + (next_edge,))
                    continue

                # exclude what we _don't_ want to visit
                if not part2:
                    # only skip if lowercase and already present
                    if next_edge.islower() and next_edge in path:
                        continue
                else:
                    # skip lowercase if there's one that's present twice and this one is present
                    if next_edge.islower():
                        small_counts = Counter(edge for edge in path if edge.islower())
                        if max(small_counts.values()) > 1 and next_edge in small_counts:
                            continue

                next_paths.add(path + (next_edge,))
        if not next_paths:
            break

        paths = next_paths

    res = len(complete_paths)

    return res


if __name__ == "__main__":
    testinp = open('day12.testinp').read()
    print(day12(testinp), day12(testinp, part2=True))
    inp = open('day12.inp').read()
    print(day12(inp), day12(inp, part2=True))
