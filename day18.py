import re
from itertools import product
from ast import literal_eval
from functools import reduce
from collections import deque

class Pair:
    def __init__(self, expr, parent=None, level=0):
        self.parent = parent
        self.level = level
        self.children = [
            subexpr if isinstance(subexpr, int) else Pair(subexpr, self, level + 1)
            for subexpr in expr
        ]

    def listify(self):
        sublists = [
            child if isinstance(child, int) else child.listify()
            for child in self.children
        ]
        return sublists

    def max_level(self):
        return max(child.max_level() for child in self.children if isinstance(child, Pair))

    def max_value(self):
        return max(child if isinstance(child, int) else child.max_value() for child in self.children)

    def magnitude(self):
        vals = [child if isinstance(child, int) else child.magnitude() for child in self.children]
        return 3*vals[0] + 2*vals[1]

    def reduce(self):
        int_finder = re.compile(r'\d+')
        pair_finder = re.compile(r'\[\d+,\d+\]')
        expr = str(self)
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
                consumer = deque(maxlen=1)
                consumer.append(None)
                consumer.extend(leading_ints)
                last_leading = consumer.pop()

                first_pair = pair_finder.search(expr, pos=start_index)
                trailing_ints = int_finder.finditer(expr, pos=first_pair.end())
                first_trailing = next(trailing_ints, None)
                first, second = map(int, int_finder.findall(first_pair.group()))

                # increment right number, if any
                if first_trailing is not None:
                    ifrom, ito = first_trailing.span()
                    new_value = int(first_trailing.group()) + second
                    expr = expr[:ifrom] + str(new_value) + expr[ito:]
                # remove pair
                ifrom, ito = first_pair.span()
                expr = expr[:ifrom] + '0' + expr[ito:]
                # increment left number, if any
                if last_leading is not None:
                    ifrom, ito = last_leading.span()
                    new_value = int(last_leading.group()) + first
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
                # we're done
                break
        return Pair(literal_eval(expr), self.parent, self.level)

    def __str__(self):
        return str(self.listify()).replace(" ","")

    def __repr__(self):
        return 'Pair with ' + str(self)

    def __add__(self, other):
        # merge and reduce
        root = Pair([self.listify(), other.listify()]).reduce()
        return root

    def __eq__(self, other):
        return self.listify() == other.listify()


def day18(inp):
    exprs = map(literal_eval, inp.splitlines())
    nums = [Pair(expr) for expr in exprs]
    total = reduce(Pair.__add__, nums)
    part1 = total.magnitude()

    part2 = max((pair1 + pair2).magnitude() for pair1, pair2 in product(nums, repeat=2))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day18.testinp').read()
    print(*day18(testinp))
    inp = open('day18.inp').read()
    print(*day18(inp))
