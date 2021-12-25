from collections import defaultdict
from operator import itemgetter
from heapq import heappush, heappop, heapify

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
    max_depth = max(tiles)[0]
    target = {
        (depth, 2*i + 1): kind
        for i, kind in enumerate('ABCD', 1)
        for depth in range(2, max_depth + 1)
    }
    rooms = {kind: index[1] for index, kind in target.items()}

    # # try to give an upper bound to cost
    # # upper bound for cost: move everyone to a further corner, then to the bottom of their rooms
    # corners = [(1, 1), (1, 11)]
    # cost_upper_bound = 0
    # for pos, kind in poses.items():
    #     goal = (max_depth, rooms[kind])
    #     potential_costs = [
    #         type_costs[kind]*(steps[pos, corner] + steps[corner, goal])
    #         for corner in corners
    #     ]
    #     cost_upper_bound += max(potential_costs)
    # cost_upper_bound = cost_upper_bound*2//3  # fudge factor; result seems safe from part1, and part2 testinp
    # print(cost_upper_bound)


    all_costs = {tuple(sorted(poses.items())): 0}  # tuple of dict items -> cost mapping
    start = tuple(sorted(poses.items()))
    initial_cost_bound = cost_lower_bound(start, target, type_costs, steps, rooms)
    #all_cost_bounds = {tuple(sorted(poses.items())): initial_cost_bound}  # tuple of dict items -> cost mapping
    #edges = {(initial_cost_bound, start)}  # set of (cost lower bound, edge state) tuples
    edges = [(initial_cost_bound, start)]  # heapq of (cost lower bound, edge state) tuples
    #edges = {start: initial_cost_bound}  # dict of positions -> cost estimate mapping
    it = 0
    while edges:
        # TODO DEBUG tmp FIXME:
        it += 1
        #edges = [(cost, poses) for poses, cost in dict((p, c) for c, p in sorted(edges)).items()]
        #heapify(edges)
        # assert len(edges) == len({start for cost, start in edges}), (len(edges), len({start for cost, start in edges})) # no duplicate positions
        # take the cheapest step
        #edge, cost_estimate = min(edges.items(), key=itemgetter(1))
        cost_estimate, edge = heappop(edges)
        cost_now = all_costs[edge]  # actual cost of reaching "edge"
        #print(f'Cost now: {cost_now}, {cost_estimate}...')
        edge_dict = dict(edge)
        poses = dict(edge).keys()

        #print_poses(edge_dict, tiles)

        # explore new states accessible from this step
        empty_tiles = tiles - poses
        for pos, kind in edge:
            # consider moving this animal

            # if this is in the right place, don't touch it
            if pos[0] > 1 and pos[1] == rooms[kind]:
                if pos[0] == max_depth:
                    # we're at the bottom
                    continue
                if all(edge_dict.get((i, pos[1]), '') == kind for i in range(pos[0] + 1, max_depth + 1)):
                    # we're on top of the right kind(s); also done
                    continue
            for next_pos in empty_tiles:
                if blockers[pos, next_pos] & poses:
                    # we can't move there due to blocker
                    continue

                # animals in hallways can only move to their destination
                if pos[0] == 1:
                    if next_pos[0] == 1 or next_pos[1] != rooms[kind]:
                        # this is not our room
                        continue
                    if any(edge_dict.get((i, next_pos[1]), kind) != kind for i in range(next_pos[0] + 1, max_depth + 1)):
                        # there are impostors inside
                        continue
                elif next_pos[0] != 1:
                    # we also have to enter the hallway when moving from one room to another
                    if next_pos[1] != pos[1] and next_pos[0] < max_depth:
                        if any(edge_dict.get((i, next_pos[1]), kind) != kind for i in range(next_pos[0] + 1, max_depth + 1)):
                            # there are impostors inside
                            continue
                
                # _now_ we have a potential move from pos to next_pos
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
                #if hashable_next_poses in all_cost_bounds:
                #    if all_cost_bounds[hashable_next_poses] < new_cost_bound:
                #        # we were here before and better
                #        # (probably won't happen)
                #        assert False
                #        continue
                #    assert False, (edges, hashable_next_poses)
                # TODO: revisit or remove this:
                # if new_cost >= cost_upper_bound:
                #     # this has to be a bad path
                #     continue

                ## DEBUG TODO REMOVE: plot move
                #print_poses(poses, tiles)
                #print_poses(next_poses, tiles)
                #print()
                #input()

                # _now_ it's worth moving from pos to next_pos
                if next_poses == target:
                    #print(f'Best cost for target: {cost}')
                    print(it, 'iterations')
                    return new_cost
                all_costs[hashable_next_poses] = new_cost
                #all_cost_bounds[hashable_next_poses] = new_cost_bound
                cost_estimate = new_cost + new_cost_bound
                heappush(edges, (cost_estimate, hashable_next_poses))
        
        if not it % 10_000:
            # prune duplicate positions in the heap (slow but saves memory)
            before = len(edges)
            edges = [(cost, poses) for poses, cost in dict((p, c) for c, p in sorted(edges)).items()]
            after = len(edges)
            print(f'pruning... {before} -> {after}')
            #print(f'cost range: {min(edges)[0]} -> {max(edges)[0]}')
            heapify(edges)

        # # heuristic: prune 10% costliest edges...
        # # (20% works for example, not for real data)
        # costs = sorted((all_costs[edge], edge) for edge in edges)
        # n_drop = len(costs)*10//100
        # #print([item[0] for item in costs]); input()
        # edges = {item[1] for item in costs[:-n_drop]}


def print_poses(poses, tiles):
    x_size = max(tiles)[0] + 1
    import numpy as np
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
    #print(day23(testinp), day23(testinp, part2=True))
    inp = open('day23.inp').read()
    #print(day23(inp), day23(inp, part2=True))

    #print(day23(testinp, part2=False))
    # 24 seconds with fixed heuristic and printing
    # 17 seconds with fixed heuristic and no printing
    # 11 seconds with _really_ fixed heuristic and no printing
    # 1.3 seconds with heapq
    print(day23(inp, part2=False))
    # 19 minutes with buggy heuristic
    # 6 minutes 10 seconds with fixed heuristic
    # 6.5 seconds with heapq; duplicate edges and huge memory need
    # 5.6 seconds with heapq; pruning duplicates every 10_000 edges

    #print(day23(testinp, part2=True))
    #print(day23(inp, part2=True))
