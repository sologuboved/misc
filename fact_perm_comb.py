def calculate_factorial(r):
    a = 1
    for i in range(2, r + 1):
        a *= i
    if r != 0:
        return float(a)
    else:
        return 1.0


def count_permutations(outcomes, length):
    return calculate_factorial(outcomes) / calculate_factorial(outcomes - length)


def count_combinations(outcomes, length):
    return count_permutations(outcomes, length) / calculate_factorial(length)


if __name__ == "__main__":
    print count_combinations(5, 2)
