"""
Converts across bases <= 16
E.g.:
print Number('215', 10).convert(16)
'215' is the number to convert (must be string)
10 is its base (must be integer)
16 is the target base (must be integer)
"""


class Number(object):

    def __init__(self, num, own_base):
        self._num = num
        self._own_base = own_base
        self._target_base = None
        self._str2num, self._num2str = self.get_alphabets()

    @staticmethod
    def get_alphabets():
        alphabet = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
        alphabet.update({str(item): item for item in range(10)})
        return alphabet, {item[1]: item[0] for item in alphabet.items()}

    def convert(self, target_base):
        self._target_base = target_base
        if self._own_base == 10:
            return self.dec2other(int(self._num))
        if self._target_base == 10:
            return self.other2dec()
        return self.dec2other(int(self.other2dec()))

    def other2dec(self):
        length = len(self._num)
        decimal = 0
        for indx in range(length):
            degree = len(self._num) - indx - 1
            decimal += self._str2num[self._num[indx]] * self._own_base ** degree
        return str(decimal)

    def dec2other(self, num):
        quotient = num / self._target_base
        if quotient == 0:
            return self._num2str[num]
        bit = num % self._target_base
        return self.dec2other(quotient) + self._num2str[bit]


if __name__ == '__main__':
    print Number('10000000', 2).convert(10)
