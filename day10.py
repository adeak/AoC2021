def day10(inp):
    rows = inp.strip().splitlines()

    scores = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    pairs = dict(zip('({[<)}]>', ')}]>({[<'))

    part1 = 0
    incompletes = []
    for row in rows:
        stack = []
        for c in row:
            if c in '[({<':
                stack.append(c)
            elif stack[-1] == pairs[c]:
                stack.pop()
            else:
                error_score = scores[c]
                part1 += error_score
                break
        else:
            incompletes.append(stack)

    scores2 = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    all_scores = []
    for row in incompletes:
        suffix = [pairs[c] for c in row[::-1]]
        contrib = 0
        for c in suffix:
            contrib *= 5
            contrib += scores2[c]
        all_scores.append(contrib)

    part2 = sorted(all_scores)[len(all_scores)//2]

    return part1, part2


if __name__ == "__main__":
    testinp = open('day10.testinp').read()
    print(*day10(testinp))
    inp = open('day10.inp').read()
    print(*day10(inp))
