class SingleNumber (object):
    def __init__(self, number):
        self.number = number
        self.factored_number = list()
        self.number_sign = 1

    def fix_sign(self):
        if self.number < 0:
            self.number_sign = -1
            self.number = abs(self.number)

    def factor_it(self):
        self.run_factory()
        return self.factored_number

    def run_factory(self):
        for candidate in range(2, self.number):
            if self.number % candidate == 0:
                for n in range(2, candidate):
                    if candidate % n == 0:
                        break
                else:
                    self.factored_number.append(candidate)
                    self.number //= candidate
                    self.run_factory()
                    break
        else:
            self.factored_number.append(self.number)


class WholeFraction(object):
    def __init__(self, lst):
        self.fraction = [SingleNumber(lst[0]), SingleNumber(lst[1])]

    def reduce_it(self):
        for n in self.fraction:
            n.fix_sign()
        if self.fraction[0] == self.fraction[1]:
            return [1 * self.fraction[0].number_sign,
                    1 * self.fraction[1].number_sign]
        else:
            reduced_numerator = list(self.fraction[0].factor_it())
            reduced_denominator = list(self.fraction[1].factor_it())
        for item in self.fraction[0].factored_number:
            for element in self.fraction[1].factored_number:
                if item == element and item in reduced_numerator and element in reduced_denominator:
                    reduced_numerator.remove(item)
                    reduced_denominator.remove(element)
                    break
        return [self.multiply(reduced_numerator) * self.fraction[0].number_sign,
                self.multiply(reduced_denominator) * self.fraction[1].number_sign]

    def multiply(self, lst):
        derivative = 1
        if len(lst) > 0:
            for item in lst:
                derivative *= item
        return derivative


def get_numbers():
    while True:
        inp = raw_input("Key in one # or two #s that constitute a fraction (space separated) or 's' for 'stop': ")
        if inp == 's':
            break
        inp = inp.split()
        if '0' in inp:
            print "No zeros"
            continue
        try:
            inp = map(int, inp)
        except ValueError:
            print "Has to be integer ot 's'"
            continue
        if len(inp) == 1:
            subj = SingleNumber(inp[0])
            print "Factored %r: %r" % (inp[0], subj.factor_it())
        elif len(inp) == 2:
            subj = WholeFraction(inp)
            res = subj.reduce_it()
            print "Reduced %r/%r: %r/%r" % (inp[0], inp[1], res[0], res[1])
        else:
            print "Too many or too few numbers"


if __name__ == "__main__":
    get_numbers()