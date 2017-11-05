import random


def factor_c(c):
    factors = list()
    for number in range(1, abs(c) + 1):
        if abs(c) % number == 0:
            factors.append([number, c / number])
    for i in range(len(factors)):
        factors.append([factors[i][0] * -1, factors[i][1] * -1])
    return factors


def factor_polynom(a, b, factored_c, test):
    ind = 0
    for item in factored_c:
        ind += 1
        if b == a * item[0] + item[1]:
            if test:
                return {'f': item[1], 'g': item[0]}
            return '(' + str(a) + "x + (" + str(item[1]) + ")) * (x + (" + str(item[0]) + '))'
    else:
        return 'Impossible'


def make_factored_polynoms(number, border):
    factored_polynoms = list()
    count = 1
    numbers = range(-border, 0) + range(1, border + 1)
    while count <= number:
        factored_polynoms.append({'a': random.choice(numbers),
                                  'f': random.choice(numbers),
                                  'g': random.choice(numbers)})
        count += 1
    return factored_polynoms


def make_polynoms(lst):
    polynoms = list()
    for item in lst:
        polynoms.append({'a': item['a'],
                         'b': item['a'] * item['g'] + item['f'],
                         'c': item['f'] * item['g']})
    return polynoms


def launch_factory(a, b, c, test=False):
    return factor_polynom(a, b, factor_c(c), test)


def run_tests(number, border):
    mfp = make_factored_polynoms(number, border)
    p = make_polynoms(mfp)
    for i in range(number):
        print '-' + str(i + 1) + '-'
        print mfp[i], '\t', p[i], '\t', launch_factory(p[i]['a'], p[i]['b'], p[i]['c'], True)


if __name__ == "__main__":
    # run_tests(5, 10)
    # print
    print launch_factory(1, -2, 4)
