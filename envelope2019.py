from operator import add, sub


class Envelope:
    def __init__(self, source, target):
        self.target = target
        self.source = source
        self.matrix = self.get_matrix()
        self.res = str()
        self.inversion_count = 3
        self.vertical = False
        self.num_steps = 1

    def unseal(self):
        count = 0
        y = 1004
        x = len(self.matrix[y]) // 2
        self.res += self.matrix[y][x]
        while True:
            print('\r{}'.format(count), end=str(), flush=True)
            count += 1
            for next_x, next_y in self.get_indices(x, y):
                try:
                    self.res += self.matrix[next_y][next_x]
                except IndexError:
                    self.write()
                    return
            x, y = next_x, next_y

    def get_indices(self, x, y):
        if self.inversion_count > 1:
            increment = sub
        else:
            increment = add
        if self.vertical:
            indices = [(x, increment(y, step)) for step in range(1, self.num_steps + 1)]
        else:
            indices = [(increment(x, step), y) for step in range(1, self.num_steps + 1)]
            self.num_steps += 4
        self.inversion_count = (self.inversion_count + 1) % 4
        self.vertical = not self.vertical
        return indices

    def get_matrix(self):
        with open(self.source, 'r') as source:
            return source.readlines()

    def write(self):
        with open(self.target, 'w') as target:
            target.write(self.res)


if __name__ == '__main__':
    Envelope('envelope2019.txt', 'envelope_script2019.py').unseal()
