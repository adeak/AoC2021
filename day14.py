from collections import Counter

def day14(inp):
    it = iter(inp.splitlines())

    template = next(it)
    next(it)
    rules = dict(row.split(' -> ') for row in it)

    # get pair counts
    pair_counts = Counter(template[ind:ind+2] for ind in range(len(template) - 1))

    # rules to generate new pairs
    pair_rules = {pair: [pair[0] + insert, insert + pair[1]] for pair, insert in rules.items()}

    polymer_counts = pair_counts
    for i in range(40):
        next_counts = Counter()
        for pair, count in polymer_counts.items():
            if pair in pair_rules:
                # we only have to add the two new pairs
                for replacing_pair in pair_rules[pair]:
                    next_counts[replacing_pair] += count
            else:
                # we keep the original pair
                next_counts[pair] += count

        polymer_counts = next_counts

        if i == 9:
            pair1_counts = polymer_counts

    # convert pair counts to letter counts
    parts = []
    for counts in pair1_counts, polymer_counts:
        letter_counts = Counter()
        for pair, freq in counts.items():
            # count the first letter of each pair
            letter_counts[pair[0]] += freq
        # edge case: last letter is missing this way
        letter_counts[template[-1]] += 1

        ranked = sorted(letter_counts.values())
        res = ranked[-1] - ranked[0]
        parts.append(res)

    return parts


if __name__ == "__main__":
    testinp = open('day14.testinp').read()
    print(*day14(testinp))
    inp = open('day14.inp').read()
    print(*day14(inp))
