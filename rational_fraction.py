# a = Rational(1, 2)
# b = Rational(5, 7)
# c = a + b
# print c


class Rational(object):

    def __init__(self, numerator, denominator):
        assert denominator != 0, "cannot divide by zero"
        self.numerator = numerator
        self.denominator = denominator
        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

    def __add__(self, fraction):
        new_numerator = self.numerator * fraction.denominator + self.denominator * fraction.numerator
        new_denominator = self.denominator * fraction.denominator
        return Rational(new_numerator, new_denominator).cancel_fraction()

    def __str__(self):
        if self.numerator == 0:
            return '0'
        return str(self.numerator) + " / " + str(self.denominator)

    def cancel_fraction(self):
        if self.numerator == 0:
            return self
        gcd = find_gcd(abs(self.numerator), abs(self.denominator))
        return Rational(self.numerator / gcd, self.denominator / gcd)


def find_gcd(num1, num2):
    if num1 < num2:
        num1, num2 = num2, num1
    remainder = num1 % num2
    if remainder == 0:
        return num2
    return find_gcd(num2, remainder)


# print find_gcd(25, 25)
a = Rational(1, 2)
b = Rational(1, -4)
c = a + b
print c
