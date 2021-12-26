from collections import defaultdict
from heapq import heappush, heappop

def day23(inp, part2=False):
    type_costs = dict(zip('ABCD', [1, 10, 100, 1000]))

    if part2:
        add_rows = [
            '  #D#C#B#A#  ',
            '  #D#B#A#C#  ',
        ]
        inp = inp.splitlines()
        inp = '\n'.join(inp[:3] + add_rows + inp[3:])

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

    # try A* searching for the cheapest path
    # a single state is a dict of (i, j) -> type items, with length 8 (or 16)
    # (well, converted to a tuple of the dict items for hashability)
    max_depth = max(tiles)[0]
    target = {
        (depth, 2*i + 1): kind
        for i, kind in enumerate('ABCD', 1)
        for depth in range(2, max_depth + 1)
    }  # the end state we're searching for
    rooms = {kind: index[1] for index, kind in target.items()}  # type -> room column mapping

    all_costs = {tuple(sorted(poses.items())): 0}  # tuple of dict items -> cost mapping
    start = tuple(sorted(poses.items()))
    initial_cost_bound = cost_lower_bound(start, target, type_costs, steps, rooms)  # lower bound for total cost
    edges = [(initial_cost_bound, start)]  # heapq of (cost lower bound, edge state) tuples
    while edges:
        cost_estimate, edge = heappop(edges)
        cost_now = all_costs[edge]
        edge_dict = dict(edge)
        poses = dict(edge).keys()

        # explore new states accessible from this step
        empty_tiles = tiles - poses

        valid_moves = []  # (pos, next_pos) tuples collected for a given state

        # first check if we can move someone to their room (either from hallway or other room)
        for pos, kind in edge:
            target_col = rooms[kind]

            if pos[0] > 1 and pos[1] == target_col:
                # we're in the right room, no need/possibility to move to right place now
                continue

            # check if the room is free
            found_valid = False
            for next_depth in range(max_depth, 1, -1):
                next_pos = (next_depth, target_col)
                if edge_dict.get(next_pos, kind) != kind:
                    # there's an impostor inside, abort
                    break
                if edge_dict.get(next_pos, '') == kind:
                    # position is filled with correct kind
                    continue
                if next_pos not in poses:
                    # this is a valid occupancy, check if we can go there
                    if blockers[pos, next_pos] & poses:
                        # can't go there
                        break
                    found_valid = True
                    break
            if found_valid:
                # then we should move pos -> next_pos
                valid_moves.append((pos, next_pos))

        # if there were valid moves here: don't try room -> hallway moves (heuristic)
        if not valid_moves:
            # gather all room -> hallway moves
            targets = {tile for tile in empty_tiles if tile[0] == 1}

            for room_col in 3, 5, 7, 9:
                # find topmost occupant
                for depth in range(2, max_depth + 1):
                    pos = (depth, room_col)
                    if pos in poses:
                        break
                else:
                    # room is empty
                    continue

                # make sure we're not trying to move someone already in the right place
                if all(edge_dict.get((d, room_col), '') == target[(d, room_col)] for d in range(depth, max_depth + 1)):
                    continue

                # move this animal to each possible hallway tile
                for hallway_tile in targets:
                    bounds = sorted([pos[1], rooms[edge_dict[pos]]])
                    if bounds[0] < hallway_tile[1] < bounds[1]:
                        # don't stop mid-way between starting room and target room
                        continue
                    if not blockers[pos, hallway_tile] & poses:
                        # the way is free
                        valid_moves.append((pos, hallway_tile))

        # now add all the valid moves (unless it's worse than before)
        for pos, next_pos in valid_moves:
            kind = edge_dict[pos]
            new_cost = cost_now + type_costs[kind]*steps[pos, next_pos]
            next_poses = {
                tmp_pos if tmp_pos != pos else next_pos: tmp_type
                for tmp_pos, tmp_type in edge
            }
            hashable_next_poses = tuple(sorted(next_poses.items()))
            old_cost = all_costs.get(hashable_next_poses, float('inf'))
            if new_cost >= old_cost:
                # we were here before and now it's not better at all
                continue
            new_cost_bound = cost_lower_bound(next_poses, target, type_costs, steps, rooms)

            # _now_ it's worth moving from pos to next_pos
            if next_poses == target:
                # we're done
                return new_cost

            # otherwise add this state to the edges
            cost_estimate = new_cost + new_cost_bound
            all_costs[hashable_next_poses] = new_cost
            heappush(edges, (cost_estimate, hashable_next_poses))


def print_poses(poses, tiles):
    """
    Quick and dirty board printing.

    This takes a dict of position -> kind items, and a set of
    valid tiles. Walls and invalid tiles are not printed.
    """
    import numpy as np  # out of laziness
    x_size = max(tiles)[0] + 1
    arr = np.full((x_size, 13), fill_value=' ')
    for one_pos, kind in poses.items():
        arr[one_pos] = kind
    for tmp_tile in tiles - poses.keys():
        arr[tmp_tile] = '.'
    print('\n'.join(''.join(row) for row in arr))


def find_path(adjacency, start, end):
    """Find a path (ignoring animals) between two tiles."""
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


def cost_lower_bound(hashable_state, target, type_costs, steps, rooms):
    """
    Give a lower bound for the lowest cost from state to target.

    Estimation: measure cost of moving each animal to the topmost
    tile of their respective rooms, ignoring all other animals.

    """
    if isinstance(hashable_state, dict):
        hashable_state = hashable_state.items()

    cost_bound = 0
    for pos, kind in hashable_state:
        if pos[0] >= 2 and pos[1] == rooms[kind]:
            # we're in the right room, might not have to move at all
            continue
        cost_bound += type_costs[kind] * steps[pos, (2, rooms[kind])]
    return cost_bound


if __name__ == "__main__":
    testinp = open('day23.testinp').read()
    print(day23(testinp), day23(testinp, part2=True))
    inp = open('day23.inp').read()
    print(day23(inp), day23(inp, part2=True))
