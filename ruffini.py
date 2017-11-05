def divide(*arg):
    """The arguments must be listed as follows, comma separated:
    all coefficients of the polynomial
    from the highest power of x to the smallest, including zeroes;
    the 2nd coefficient of the divisor.
    E.g.: (1 + 4x^2 - 2x^4 - 7x^3) / (x + 4) -->
    --> divide(-2, -7, 4, 0, 1, 4)
    """
    start = list(arg)
    a = -start.pop(-1)
    print make_string(start) + "divided by x + (%d)\n" % -a
    finish = [start[0]]
    for ind in range(len(start) - 1):
        finish.append(finish[ind] * a + start[ind + 1])
    r = finish.pop(-1)
    print "=", make_string(finish)
    print "+ %d / (x + (%d)" % (r, -a)
    print "(remainder = %d)" % r


def make_string(lst):
    dem = ''
    for ind in range(len(lst)):
        dem = ('(' + str(lst[len(lst) - ind - 1]) + "x^" + str(ind) + ')') + ' + ' + dem
    return dem[: -2]


if __name__ == "__main__":
    divide(-2, -7, 4, 0, 1, 4)