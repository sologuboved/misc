import math
from quadr_factory import make_factored_polynoms
from quadr_factory import make_polynoms


class Equation(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.discr = float(self.b ** 2 - 4 * self.a * self.c)

    def find_solution(self, full):
        if self.discr < 0:
            return "No real solutions"
        if self.discr == 0 and full < 3:
            return "%r / %r" % (-self.b, 2 * self.a)
        if full == 0:
            return "(%r +/- sqrt(%r)) / %r" % (-self.b, self.discr, 2 * self.a)
        if full == 1:
            return "%r / %r, %r / %r" % (-self.b + math.sqrt(self.discr),
                                         2 * self.a,
                                         -self.b - math.sqrt(self.discr),
                                         2 * self.a)
        if full == 2:
            if self.discr == 0:
                return -self.b / (2 * self.a)
            else:
                x1 = (-self.b + math.sqrt(self.discr)) / (2 * self.a)
                x2 = (-self.b - math.sqrt(self.discr)) / (2 * self.a)
                return x1, x2


def launch(a, b, c, discr=False, fullness=2):
    if discr:
        print(Equation(a, b, c).discr)
    else:
        print(Equation(a, b, c).find_solution(fullness))


def run_tests(number, border, fullness=2):
    mfp = make_factored_polynoms(number, border)
    p = make_polynoms(mfp)
    for i in range(number):
        print('-' + str(i + 1) + '-')
        print(mfp[i], '\t', p[i], '\t', Equation(p[i]['a'], p[i]['b'], p[i]['c']).find_solution(fullness))


if __name__ == "__main__":
    run_tests(5, 10)
    launch(3, -11, -4, False, 1)
    launch(-1, 5, 36, True)
