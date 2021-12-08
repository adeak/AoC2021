def day08(inp):
    rows = inp.strip().splitlines()
    part1 = part2 = 0
    for row in rows:
        # represent patterns and displayed digits as lists of sets of characters
        patterns, _, digits = row.partition(' | ')
        patterns = {frozenset(pattern) for pattern in patterns.split()}
        digits = [frozenset(digit) for digit in digits.split()]

        # identify known patterns
        one, seven, four, eight = known_digits = [get_digits_by_length(patterns, n)[0] for n in [2, 3, 4, 7]]
        part1 += sum(1 for digit in digits if digit in known_digits)

        patterns -= set(known_digits)

        # "6" + "1" = "8" only true for "6"
        six = next(pattern for pattern in patterns if pattern | one == eight)
        patterns.remove(six)

        # remaining 6-segment digits: "0" and "9", and only "9" contains "4"
        six_segments = get_digits_by_length(patterns, 6)
        for digit in six_segments:
            if four < digit:
                nine = digit
            else:
                zero = digit
        patterns -= {zero, nine}

        # remaining: 5 segment digits, "2", "3", "5"
        # "2" + "4" = "8" only for "2"
        # only "3" contains "1"
        two = next(pattern for pattern in patterns if pattern | four == eight)
        three = next(pattern for pattern in patterns if one < pattern)
        patterns -= {two, three}
        five = patterns.pop()

        digit_list = [zero, one, two, three, four, five, six, seven, eight, nine]
        proper_digits = (digit_list.index(digit) for digit in digits)
        part2 += int(''.join(map(str, proper_digits)))

    return part1, part2


def get_digits_by_length(patterns, length):
    """Find all digits of a given length."""
    return [pattern for pattern in patterns if len(pattern) == length]


if __name__ == "__main__":
    testinp = open('day08.testinp').read()
    print(*day08(testinp))
    inp = open('day08.inp').read()
    print(*day08(inp))
