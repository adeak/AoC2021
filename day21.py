from itertools import cycle, count, islice, product
from collections import Counter, defaultdict

def day21(inp):
    initial_poses = [int(row.split()[-1]) for row in inp.splitlines()]
    player_indices = [0, 1]

    # part 1
    die = cycle(range(1, 101))
    poses = initial_poses.copy()
    scores = [0, 0]
    roll_count = 0
    part1 = None
    for i in count(1):
        for index in player_indices:
            increment = sum(islice(die, 3))
            roll_count += 3
            poses[index] = ((poses[index] + increment) - 1) % 10 + 1
            scores[index] += poses[index]
            if scores[index] >= 1000:
                loser_score = scores[1 - index]
                part1 = loser_score * roll_count
                break
        if part1:
            break

    # part 2
    # the multiplicity of a given roll triple
    stats = Counter([i + j + k for i, j, k in product([1, 2, 3], repeat=3)])
    poses_scores = {tuple(initial_poses) + (0, 0): 1}  # each element is a universe equivalence class
    winning_counts = [0, 0]  # for each player in all universes
    for i in count(1):
        for index in player_indices:
            new_poses_scores = defaultdict(int)
            for roll, roll_multi in stats.items():
                for pos_score, player_multi in poses_scores.items():
                    poses, scores = pos_score[:2], pos_score[2:]
                    new_pos = ((poses[index] + roll) - 1) % 10 + 1
                    new_score_contrib = new_pos
                    new_score = scores[index] + new_score_contrib
                    total_multiplicity = player_multi * roll_multi
                    if new_score >= 21:
                        winning_counts[index] += total_multiplicity
                        continue
                    # otherwise keep track of this universe equivalence class
                    if index == 0:
                        new_poses = new_pos, poses[1]
                        new_scores = new_score, scores[1]
                    else:
                        new_poses = poses[0], new_pos
                        new_scores = scores[0], new_score
                    # watch out for overlapping future timelines!
                    new_poses_scores[new_poses + new_scores] += total_multiplicity
            poses_scores = new_poses_scores
            if not poses_scores:
                # games over
                break
        if not poses_scores:
            break
    part2 = max(winning_counts)

    return part1, part2


if __name__ == "__main__":
    testinp = open('day21.testinp').read()
    print(*day21(testinp))
    inp = open('day21.inp').read()
    print(*day21(inp))
