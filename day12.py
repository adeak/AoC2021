from collections import defaultdict, Counter

def day12(inp):
    conn_aux = [row.split('-') for row in inp.splitlines()]
    conn = defaultdict(set)
    for src, dest in conn_aux:
        conn[src].add(dest)
        conn[dest].add(src)
    conn = dict(conn)

    root = 'start'
    paths = {(root,)}
    complete_paths = set()
    while True:
        next_paths = set()
        for path in paths:
            for next_edge in conn[path[-1]]:
                if next_edge == 'start':
                    continue
                if next_edge == 'end':
                    complete_paths.add(path + (next_edge,))
                    continue
                if next_edge.islower() and next_edge in path:
                    continue
                next_paths.add(path + (next_edge,))
        if not next_paths:
            break
        paths = next_paths

    part1 = len(complete_paths)

    root = 'start'
    paths = {(root,)}
    complete_paths = set()
    while True:
        next_paths = set()
        for path in paths:
            for next_edge in conn[path[-1]]:
                if next_edge == 'start':
                    continue
                if next_edge == 'end':
                    complete_paths.add(path + (next_edge,))
                    continue
                if next_edge.islower():
                    small_counts = Counter([edge for edge in path if edge.islower()])
                    if max(small_counts.values()) > 1 and next_edge in small_counts:
                        continue
                next_paths.add(path + (next_edge,))
        if not next_paths:
            break
        paths = next_paths

    part2 = len(complete_paths)

    return part1, part2


if __name__ == "__main__":
    testinp = open('day12.testinp').read()
    print(*day12(testinp))
    inp = open('day12.inp').read()
    print(*day12(inp))
