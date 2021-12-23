from collections import defaultdict

def day23(inp):
    part1 = part2 = None
    type_costs = dict(zip('ABCD', [1, 10, 100, 1000]))

    # read in map
    tiles = set()  # (i, j) indices
    poses = {}  # (i, j) -> type
    for i, row in enumerate(inp.splitlines()):
        for j, c in enumerate(row):
            if c in '# ':
                continue
            tiles.add((i, j))
            if c in type_costs:
                poses[i, j] = c

    # build adjacency graph
    adjacency = defaultdict(list)
    for tile in tiles:
        deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for delta in deltas:
            other = tile[0] + delta[0], tile[1] + delta[1]
            if other in tiles:
                adjacency[tile].append(other)

    # explore blockers from each position to each position
    steps = {}  # (i, j), (k, l) -> number of steps to walk from start to end
    blockers = {}  # (i, j), (k, l) -> list of blocking indices from start to end
    tiles_lst = list(tiles)
    for i, start in enumerate(tiles_lst):
        for end in tiles_lst[i + 1:]:
            path = find_path(adjacency, start, end)
            n_steps = len(path)
            blockers[start, end] = blockers[end, start] = set(path[:-1])  # omit end in blockers
            steps[start, end] = steps[end, start] = n_steps

    # remove forbidden tiles
    tiles -= {(1, y) for y in [3, 5, 7, 9]}

    # explore the state space
    # a single state is a dict of (i, j) -> type items, with length 8
    # there are 190466640 distinct states, but most of them can't be explored cheaply
    # (even fewer without forbidden tiles)
    all_costs = {tuple(sorted(poses.items())): 0}  # tuple of dict items -> cost
    target = {
        (2, 3): 'A',
        (3, 3): 'A',
        (2, 5): 'B',
        (3, 5): 'B',
        (2, 7): 'C',
        (3, 7): 'C',
        (2, 9): 'D',
        (3, 9): 'D',
    }
    rooms = {kind: index[1] for index, kind in target.items()}
    edges = {tuple(sorted(poses.items()))}

    # upper bound for cost: move everyone to a further corner then to the bottom of their rooms
    corners = [(1, 1), (1, 11)]
    cost_bound = 0
    for pos, kind in poses.items():
        goal = (3, rooms[kind])
        potential_costs = [
            type_costs[kind]*(steps[pos, corner] + steps[corner, goal])
            for corner in corners
        ]
        cost_bound += max(potential_costs)

    best_score = float('inf')
    while edges:
        next_edges = set()
        for edge in edges:
            poses = dict(edge)
            cost_now = all_costs[edge]
            # explore all states from here
            empty_tiles = tiles - poses.keys()
            for pos, kind in poses.items():
                # if this is in the right place, don't touch it
                if pos[0] > 1 and pos[1] == rooms[kind]:
                    if pos[0] == 3:
                        # we're at the bottom
                        ## DEBUG TODO REMOVE: plot move
                        #print(f'Skipping: {pos} {kind} in')
                        #print_poses(poses, tiles)
                        continue
                    if poses.get((3, pos[1]), '') == kind:
                        # we're on top of the right kind; also done
                        ## DEBUG TODO REMOVE: plot move
                        #print(f'Skipping: {pos} {kind} in')
                        #print_poses(poses, tiles)
                        continue
                for next_pos in empty_tiles:
                    # animals in hallways can only move to their destination
                    if pos[0] == 1:
                        if next_pos[0] == 1 or next_pos[1] != rooms[kind]:
                            # this is not our room
                            continue
                        other_index = (3 if next_pos[0] == 2 else 2, next_pos[1])
                        if poses.get(other_index, kind) != kind:
                            # there are impostors inside
                            continue
                    elif next_pos[0] != 1:
                        # we also have to enter the hallway when moving from one room to another
                        if next_pos[1] != pos[1] and next_pos[0] == 2:
                            other_index = (3, next_pos[1])
                            if poses.get(other_index, kind) != kind:
                                # there are impostors inside
                                continue
                    if blockers[pos, next_pos] & poses.keys():
                        # we can't move there due to blocker
                        continue
                    cost = cost_now + type_costs[kind]*steps[pos, next_pos]
                    next_poses = {
                        tmp_pos if tmp_pos != pos else next_pos: tmp_type
                        for tmp_pos, tmp_type in poses.items()
                    }
                    hashable_next_poses = tuple(sorted(next_poses.items()))
                    old_cost = all_costs.get(hashable_next_poses, float('inf'))
                    if cost >= old_cost:
                        # we were here before and now it's not better at all
                        continue
                    if cost >= cost_bound:
                        # this has to be a bad path
                        continue
                    
                    ## DEBUG TODO REMOVE: plot move
                    #print_poses(poses, tiles)
                    #print(poses(next_poses, tiles)
                    #print()
                    #input()

                    next_edges.add(hashable_next_poses)
                    all_costs[hashable_next_poses] = cost
                    #print(next_poses, target)
                    if next_poses == target:
                        cost_bound = cost
                        print(f'Next best cost for target: {cost}')
        edges = next_edges

        # # heuristic: prune 10% costliest edges...
        # # (20% works for example, not for real data)
        # costs = sorted((all_costs[edge], edge) for edge in edges)
        # n_drop = len(costs)*10//100
        # #print([item[0] for item in costs]); input()
        # edges = {item[1] for item in costs[:-n_drop]}

    return part1, part2


def print_poses(poses, tiles):
    import numpy as np
    arr = np.full((5, 13), fill_value=' ')
    for one_pos, kind in poses.items():
        arr[one_pos] = kind
    for tmp_tile in tiles - poses.keys():
        arr[tmp_tile] = '.'
    print('\n'.join(''.join(row) for row in arr))


def find_path(adjacency, start, end):
    comefrom = {}
    tile = start
    edges = {tile}
    while True:
        next_edges = set()
        for edge in edges:
            for neighb in adjacency[edge]:
                if neighb in comefrom:
                    # we've already been here; abort
                    continue
                comefrom[neighb] = edge
                if neighb == end:
                    # we're done
                    tile = end
                    path = []
                    while True:
                        path.append(tile)
                        tile = comefrom[tile]
                        if tile == start:
                            # note: path omits the starting point
                            return path[::-1]

                next_edges.add(neighb)
        edges = next_edges


if __name__ == "__main__":
    testinp = open('day23.testinp').read()
    print(*day23(testinp))
    inp = open('day23.inp').read()
    print(*day23(inp))
    # 18049 too high
    # 16831 too high
    # 16091 too high
