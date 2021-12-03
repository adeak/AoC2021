from collections import Counter

def day03(inp):
    rows = inp.strip().splitlines()

    freq = Counter()
    for row in rows:
        for i, val in enumerate(row):
            freq[i, val] += 1
    n = len(row)
    gamma = []
    epsilon = []
    for i in range(n):
        one_common = freq[i, '1'] > freq[i, '0']
        gamma.append(1 if one_common else 0)
        epsilon.append(0 if one_common else 1)

    gamma = sum(2**i*val for i, val in enumerate(gamma[::-1]))
    epsilon = sum(2**i*val for i, val in enumerate(epsilon[::-1]))

    return gamma * epsilon


def day03_part2(inp):
    rows = inp.strip().splitlines()
    nums_common = set(rows)
    nums_uncommon = nums_common.copy()
    n = len(rows[0])

    for i in range(n):
        if len(nums_common) > 1:
            one_common = sum(1 for num in nums_common if num[i] == '1') >= len(nums_common) / 2
            char = '1' if one_common else '0'
            nums_common = {num for num in nums_common if num[i] == char}
        if len(nums_uncommon) > 1:
            one_uncommon = sum(1 for num in nums_uncommon if num[i] == '1') < len(nums_uncommon) / 2
            char = '1' if one_uncommon else '0'
            nums_uncommon = {num for num in nums_uncommon if num[i] == char}
    gamma = nums_common.pop()
    epsilon = nums_uncommon.pop()
    assert not nums_common and not nums_uncommon

    gamma = sum(2**i*int(val) for i, val in enumerate(gamma[::-1]))
    epsilon = sum(2**i*int(val) for i, val in enumerate(epsilon[::-1]))

    return gamma * epsilon


if __name__ == "__main__":
    testinp = open('day03.testinp').read()
    print(day03(testinp))
    inp = open('day03.inp').read()
    print(day03(inp))
    print(day03_part2(testinp))
    print(day03_part2(inp))
