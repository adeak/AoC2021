def day10(inp):
    rows = inp.strip().splitlines()

    error_points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    completion_points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    matching_pair = dict(zip('({[<)}]>', ')}]>({[<'))

    part1 = 0
    incompletes = []
    for row in rows:
        stack = []
        for c in row:
            if c in '[({<':
                # open a level
                stack.append(c)
            elif stack[-1] == matching_pair[c]:
                # matching pair; forget about it
                stack.pop()
            else:
                # invalid closing bracket
                error_score = error_points[c]
                part1 += error_score
                break
        else:
            # there were no invalid closing brackets
            incompletes.append(stack)

    scores = []
    for row in incompletes:
        suffix = [matching_pair[c] for c in row[::-1]]
        score = 0
        for c in suffix:
            score *= 5
            score += completion_points[c]
        scores.append(score)

    part2 = sorted(scores)[len(scores)//2]

    return part1, part2


if __name__ == "__main__":
    testinp = open('day10.testinp').read()
    print(*day10(testinp))
    inp = open('day10.inp').read()
    print(*day10(inp))
