def day24(inp):
    # try reverse engineering
    # each digit is first read into w, and a result is accumulated in z
    #
    # first assert that each block for each digit is the same with different constants
    _, *blocks = inp.split('inp w\n')
    all_constants = []
    for all_rows in zip(*[block.strip().splitlines() for block in blocks]):
        # all_rows contains the next line of code for each digit's block
        # i.e. 14 strings like 'mul x 0'
        ref_head, ref_arg = all_rows[0].rsplit(maxsplit=1)
        arg_vals = [ref_arg if ref_arg in 'xyzw' else int(ref_arg)]
        for rest_row in all_rows[1:]:
            other_head, other_arg = rest_row.rsplit(maxsplit=1)
            assert other_head == ref_head
            if ref_arg in 'xyzw':
                assert other_arg == ref_arg
            else:
                arg_vals.append(int(other_arg))
        # if len(set(arg_vals)) == 1:
        #     print(set(arg_vals))
        # else:
        #     all_constants.append(arg_vals)
        #     print(arg_vals)

        if len(set(arg_vals)) > 1:
            all_constants.append(arg_vals)
    print(all_constants)

    # consts[0]: [ 1,  1,  1,  26,  1, 26,  1,  1,  1, 26,  26,  26, 26, 26]
    # consts[1]: [13, 11, 15, -11, 14,  0, 12, 12, 14, -6, -10, -12, -3, -5]
    # consts[2]: [13, 10,  5,  14,  5, 15,  4, 11,  1, 15,  12,   8, 14,  9]

    # so a single block looks like this:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z 1   # <- no-op | or div z 26; varied
    # add x 13  # <- varied
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    # mul y 0
    # add y w
    # add y 13  # <- varied
    # mul y x
    # add z y
    #
    # varied constants: line 5, 6, 16
    # and consts[1] is never a valid digit!
    #
    # a single block as high-level code:
    #
    #   w = digit
    #   x = z % 26 + consts[1]
    #   z //= consts[0]  # either 1 (no-op) or 26
    #   x = x != w
    #   y = 25 * x + 1  # 1 (if not x) or 26 (if x)
    #   z *= y
    #   y = (w + consts[2]) * x
    #   z += y
    #
    #
    # further optimised:
    #
    #   x = (z % 26 + consts[1])
    #   z //= consts[0]  # either 1 (no-op) or 26
    #   if digit != x:
    #       z = z*26 + digit + consts[2]  # and digit + consts[2] is never 0 and is less than 25
    #   else:
    #       z += 0  # no-op
    #
    #
    # when we have a z*26 + digit + consts[2] value from a previous digit,
    # we next compute
    #     (z % 26 + consts[1]) = 0 + digit_prev % 26 + consts_prev[2] % 26 + consts_now[1]
    #                          = digit_prev + consts_prev[2] % 26 + consts_now[1]
    #     and compare this with the next digit, i.e. history of z is lost for the check
    #
    #
    # for a given digit:
    #     assuming we can hit all the != branches:
    #     digit + consts[2] is being stored as digits of a 26-base number
    #     as long as consts[0] == 1 for the given decimal digit
    #     if consts[0] == 26 for the given decimal digit: shift down in base 26
    #         i.e. discard the previous (digit + consts[2]) value
    #     and there are 7 right shifts... suspicious
    #
    # hunch:
    #     there are exactly 7 right-shift-by-26 digits among 14
    #     and the first digit always gives z > 0
    #     and each digit includes a potential left-shift in the if
    #     so hypothesis: we can only get 0 at the end if we hit the left-shift branch at most 7 times
    #
    # algorithm:
    #     start from largest valid 14-digit number,
    #     start executing code
    #     count number of entries into the "left-shift" if branch
    #     if more than 7: need to backtrack from the given digit
    #     stop with first valid number

    def decrement_at(num, index):
        """Decrement number at digit "index" skipping zeros, set remaining digits to 9."""
        digits = list(str(num))
        digit_now = int(digits[index])
        if digit_now > 1:
            digits[index] = str(digit_now - 1)
        else:
            return decrement_at(num, index - 1)
        # set remaining digits to 9
        digits[index + 1:] = '9'*(13 - index)
        return int(''.join(digits))

    num = int('9'*14)
    while True:
        digits = map(int, str(num))
        z = 0
        leftshift_count = 0
        # all_constants is [first_constants, second_constants, third_constants]
        # (3-length list of 14-length lists)
        for i, (digit, consts) in enumerate(zip(digits, zip(*all_constants))):
            x = (z % 26 + consts[1])
            z //= consts[0]  # either 1 (no-op) or 26
            if digit != x:
                leftshift_count += 1
                if leftshift_count == 8:
                    # there's no way to shift back to 0 later
                    break
                z = z*26 + digit + consts[2]
        else:
            if z == 0:
                # we're done
                part1 = num
                break

        # decrease and backtrack:
        #     decrease the ith digit in num
        #     set digits from i+1 to 14 to 9
        num = decrement_at(num, i)

    # part 2: same just inreasing
    def increment_at(num, index):
        """Increment number at digit "index" skipping zeros, set remaining digits to 1."""
        digits = list(str(num))
        digit_now = int(digits[index])
        if digit_now < 9:
            digits[index] = str(digit_now + 1)
        else:
            return increment_at(num, index - 1)
        # set remaining digits to 1
        digits[index + 1:] = '1'*(13 - index)
        return int(''.join(digits))
    num = int('1'*14)
    while True:
        digits = map(int, str(num))
        z = 0
        leftshift_count = 0
        # all_constants is [first_constants, second_constants, third_constants]
        # (3-length list of 14-length lists)
        for i, (digit, consts) in enumerate(zip(digits, zip(*all_constants))):
            x = (z % 26 + consts[1])
            z //= consts[0]  # either 1 (no-op) or 26
            if digit != x:
                leftshift_count += 1
                if leftshift_count == 8:
                    # there's no way to shift back to 0
                    break
                z = z*26 + digit + consts[2]
        else:
            if z == 0:
                # we're done
                part2 = num
                break

        # increase and backtrack:
        num = increment_at(num, i)

    return part1, part2
    

if __name__ == "__main__":
    inp = open('day24.inp').read()
    print(day24(inp))
