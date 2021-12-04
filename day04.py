import numpy as np

def day04(inp):
    blocks = inp.strip().split('\n\n')
    nums = np.fromstring(blocks[0], sep=',', dtype=int)
    boards = np.array([np.fromstring(block, sep=' ', dtype=int).reshape(5, 5) for block in blocks[1:]])

    last_winners = set()
    for num in nums:
        # set drawn number to -1
        boards[boards == num] = -1

        # check if there's a winner
        hits = boards == -1
        wins = hits.all(1).any(-1) | hits.all(-1).any(-1)
        if wins.sum() == 1 and not last_winners:
            # part 1: first winner
            winner = boards[wins.argmax(), ...]
            part1 = winner[winner != -1].sum() * num
        if wins.sum() == wins.size == len(last_winners) + 1:
            # part 2: last winner
            winner_index = (set(range(wins.size)) - last_winners).pop()
            winner = boards[winner_index, ...]
            part2 = winner[winner != -1].sum() * num
            break

        last_winners = set(wins.nonzero()[0])
    else:
        raise ValueError('A board never wins!')

    return part1, part2


if __name__ == "__main__":
    testinp = open('day04.testinp').read()
    print(day04(testinp))
    inp = open('day04.inp').read()
    print(day04(inp))
