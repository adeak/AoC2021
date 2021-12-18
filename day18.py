import re
from itertools import product
from ast import literal_eval
from functools import reduce
from collections import deque


def magnitude(expr):
    vals = [subexpr if isinstance(subexpr, int) else magnitude(subexpr) for subexpr in expr]
    return 3*vals[0] + 2*vals[1]


def reduce_pair(pair):
    int_finder = re.compile(r'\d+')
    pair_finder = re.compile(r'\[\d+,\d+\]')
    expr = str(pair).replace(' ', '')
    while True:
        # check for explode rule
        level = 0
        start_index = 0
        for i, c in enumerate(expr):
            if c == '[':
                level += 1
            elif c == ']':
                level -= 1
            if level == 5:
                # first rule matches
                start_index = i
                break
        if start_index:
            # explode
            leading_ints = int_finder.finditer(expr, endpos=start_index)
            consumer = deque([None], maxlen=1)
            consumer.extend(leading_ints)
            last_leading_int = consumer.pop()

            first_pair = pair_finder.search(expr, pos=start_index)
            trailing_ints = int_finder.finditer(expr, pos=first_pair.end())
            first_trailing_int = next(trailing_ints, None)
            first, second = map(int, int_finder.findall(first_pair.group()))

            # increment right number, if any
            if first_trailing_int is not None:
                ifrom, ito = first_trailing_int.span()
                new_value = int(first_trailing_int.group()) + second
                expr = expr[:ifrom] + str(new_value) + expr[ito:]
            # remove pair
            ifrom, ito = first_pair.span()
            expr = expr[:ifrom] + '0' + expr[ito:]
            # increment left number, if any
            if last_leading_int is not None:
                ifrom, ito = last_leading_int.span()
                new_value = int(last_leading_int.group()) + first
                expr = expr[:ifrom] + str(new_value) + expr[ito:]
            # remove potential leading/trailing commas after pair removal
            expr = expr.replace(',]', ']').replace('[,', '[')

            continue

        # check for split rule
        intmatches = int_finder.finditer(expr)
        for intmatch in intmatches:
            value = int(intmatch.group())
            if value < 10:
                continue
            ifrom, ito = intmatch.span()
            expr = expr[:ifrom] + f'[{value//2},{-(-value//2)}]' + expr[ito:]
            break
        else:
            # expression is invariant; we're done
            break
    return literal_eval(expr)


def add(first, second):
    # merge and reduce
    return reduce_pair([first, second])


def day18(inp):
    nums = [literal_eval(row) for row in inp.splitlines()]
    total = reduce(add, nums)

    part1 = magnitude(total)
    part2 = max(magnitude(add(pair1, pair2)) for pair1, pair2 in product(nums, repeat=2))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day18.testinp').read()
    print(*day18(testinp))
    inp = open('day18.inp').read()
    print(*day18(inp))
