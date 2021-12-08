def day08(inp):
    rows = inp.strip().splitlines()
    part1 = part2 = 0
    for row in rows:
        patterns, _, digits = row.partition(' | ')
        patterns = [set(pattern) for pattern in patterns.split()]
        digits = [set(digit) for digit in digits.split()]

        # identify known patterns
        def get_digits_by_length(patterns, length):
            return [pattern for pattern in patterns if len(pattern) == length]

        one, seven, four, eight = (get_digits_by_length(patterns, n)[0] for n in [2, 3, 4, 7])
        part1 += sum(1 for digit in digits if digit in [one, seven, four, eight])

        rest = [pattern for pattern in patterns if pattern not in [one, seven, four, eight]]

        # "6" + "1" = "8" only true for "6"
        six = next(pattern for pattern in rest if pattern | one == eight)

        # remaining 6-segment digits: "0" and "9", and only "9" contains "4"
        six_segments = get_digits_by_length(patterns, 6)
        for digit in six_segments:
            if digit == six:
                continue
            if four < digit:
                nine = digit
            else:
                zero = digit
        
        rest = [pattern for pattern in rest if pattern not in [six, zero, nine]]

        # remaining: 5 segment digits, "2", "3", "5"
        # "2" + "4" = "8" only for "2"
        two = next(pattern for pattern in rest if pattern | four == eight)

        # only "3" contains "1"
        rest = [pattern for pattern in patterns if pattern not in [one, seven, four, eight, six, zero, nine, two]]
        three = next(pattern for pattern in rest if one < pattern)
        rest = [pattern for pattern in rest if pattern != three]
        five = rest[0]

        proper_digits = [[zero, one, two, three, four, five, six, seven, eight, nine].index(digit) for digit in digits]
        part2 += int(''.join(f'{digit}' for digit in proper_digits))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day08.testinp').read()
    print(*day08(testinp))
    inp = open('day08.inp').read()
    print(*day08(inp))
