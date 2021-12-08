def day08(inp):
    rows = inp.strip().splitlines()
    part1 = part2 = 0
    for row in rows:
        # represent patterns and displayed digits as lists of sets of characters
        patterns, _, digits = row.partition(' | ')
        patterns = [set(pattern) for pattern in patterns.split()]
        digits = [set(digit) for digit in digits.split()]

        # identify known patterns
        one, seven, four, eight = known_digits = [get_digits_by_length(patterns, n)[0] for n in [2, 3, 4, 7]]
        part1 += sum(1 for digit in digits if digit in known_digits)

        remove_known_digits(patterns, *known_digits)

        # "6" + "1" = "8" only true for "6"
        six = next(pattern for pattern in patterns if pattern | one == eight)
        remove_known_digits(patterns, six)

        # remaining 6-segment digits: "0" and "9", and only "9" contains "4"
        six_segments = get_digits_by_length(patterns, 6)
        for digit in six_segments:
            if four < digit:
                nine = digit
            else:
                zero = digit
        
        remove_known_digits(patterns, zero, nine)

        # remaining: 5 segment digits, "2", "3", "5"
        # "2" + "4" = "8" only for "2"
        # only "3" contains "1"
        two = next(pattern for pattern in patterns if pattern | four == eight)
        three = next(pattern for pattern in patterns if one < pattern)
        remove_known_digits(patterns, two, three)
        five = patterns.pop()

        proper_digits = [[zero, one, two, three, four, five, six, seven, eight, nine].index(digit) for digit in digits]
        part2 += int(''.join(f'{digit}' for digit in proper_digits))

    return part1, part2


def get_digits_by_length(patterns, length):
    """Find all digits of a given length."""
    return [pattern for pattern in patterns if len(pattern) == length]


def remove_known_digits(patterns, *known_digits):
    """In-place remove known digits from a list of patterns."""
    for digit in known_digits:
        patterns.remove(digit)


if __name__ == "__main__":
    testinp = open('day08.testinp').read()
    print(*day08(testinp))
    inp = open('day08.inp').read()
    print(*day08(inp))
