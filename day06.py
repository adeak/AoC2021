from collections import Counter

def day06(inp):
    nums = map(int, inp.strip().split(','))

    population = Counter(nums)

    for day in range(256):
        # map n to n-1
        # map newly created -1 to 6 plus value*8
        for old_age in range(9):
            population[old_age - 1] = population[old_age]
            population[old_age] = 0
        birth_count = population[-1]
        del population[-1]  # just to make it cleaner, not really necessary
        population[6] += birth_count
        population[8] = birth_count

        if day == 79:
            # part 1
            population_part1 = population.copy()

    part1 = sum(population_part1.values())
    part2 = sum(population.values())

    return part1, part2


if __name__ == "__main__":
    testinp = open('day06.testinp').read()
    print(*day06(testinp))
    inp = open('day06.inp').read()
    print(*day06(inp))
