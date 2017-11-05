import random
from collections import deque
from sys import exit

MINE = 'M'
UNTOUCHED = '?'


class Field(object):
    def __init__(self, y_dim, x_dim, num_mines):
        self.y_dim = y_dim
        self.x_dim = x_dim
        self.num_mines = num_mines
        self.closed = y_dim * x_dim - num_mines
        self.visited = set()
        self.user_mat = self.make_empty_mat(UNTOUCHED)
        self.mat = None

    def __getitem__(self, item):
        return self.mat[item]

    def __str__(self):
        return self.get_mat(True)

    def make_empty_mat(self, filler):
        return [[filler for _ in xrange(self.x_dim)] for _ in xrange(self.y_dim)]

    def arrange_field(self, coords):
        mines = self.make_empty_mat(0)
        mat = self.make_empty_mat(0)
        possible_pos = set((vert, hor) for vert in xrange(self.y_dim) for hor in xrange(self.x_dim))
        possible_pos = list(possible_pos - (self.find_neighbours(coords) | {coords}))
        random.shuffle(possible_pos)
        for (vert, hor) in possible_pos[: self.num_mines]:
            mines[vert][hor] = 1
        for vert in xrange(self.y_dim):
            for hor in xrange(self.x_dim):
                if mines[vert][hor] != 1:
                    count = self.count_cell((vert, hor), mines)
                else:
                    count = MINE
                mat[vert][hor] = count
        self.mat = mat
        self.is_mine(coords)

    def get_mat(self, user=False):
        if user:
            original = self.user_mat
        else:
            original = self.mat
        mat = ''
        for row in original:
            mat += (' '.join(map(str, row)) + '\n')
        return mat

    def set_cell(self, coords, count):
        vert, hor = coords
        self.user_mat[vert][hor] = count

    def find_neighbours(self, coords):
        vert, hor = coords
        possible_coords = set()
        for row in range(vert - 1, vert + 2):
            for col in range(hor - 1, hor + 2):
                if row in range(self.y_dim) and col in range(self.x_dim) and not (row == vert and col == hor):
                    possible_coords.add((row, col))
        return possible_coords

    def count_cell(self, coords, mat):
        return sum([int(mat[coord[0]][coord[1]]) for coord in self.find_neighbours(coords)])

    def is_mine(self, initial_coords):
        queue = deque([initial_coords])
        while queue:
            curr_coords = queue.popleft()
            self.visited.add(curr_coords)
            vert, hor = curr_coords
            cell = self.mat[vert][hor]
            if cell == MINE:
                return True
            if cell == 0:
                neighbours = self.find_neighbours(curr_coords)
                for neighbour in neighbours:
                    if neighbour not in self.visited:
                        queue.append(neighbour)
                        self.visited.add(neighbour)
            self.user_mat[vert][hor] = cell
            self.closed -= 1
        print "visited", self.visited


def start_game():
    while True:
        initial = raw_input("Key in height, width, number of mines (e.g 9 9 10) or 'b' for break ")
        if initial == 'b':
            exit()
        initial = initial.strip().split()
        if len(initial) != 3:
            print "Not enough or too many items"
            continue
        try:
            initial = map(int, initial)
            height, width, mines_num = initial
            if mines_num > height * width - 9 or mines_num <= 0 or height <= 0 or width <= 0:
                print "Ten points from Gryffindor"
                continue
        except:
            print "Wrong values"
            continue
        print "Here comes a %dx%d field with %d mines" % (height, width, mines_num)
        return height, width, mines_num


def make_first_move(preconditions):
    height, width, mines_num = preconditions
    new_field = Field(height, width, mines_num)
    print new_field
    while True:
        first_move = raw_input("Choose 1st cell (e.g 0 0) or 'b' for break ")
        good_move = is_valid_move(first_move, height, width)
        if not good_move:
            print "Try again"
        else:
            break
    new_field.arrange_field(good_move)
    print new_field.get_mat()
    new_field.set_cell(good_move, new_field[good_move[0]][good_move[1]])
    return new_field


def make_subsequent_moves(fieldling):
    print "Here we are"
    print "closed cells:", fieldling.closed
    print fieldling
    while fieldling.closed:
        new_move = raw_input("Choose next cell (e.g 0 0) or 'b' for break ")
        good_move = is_valid_move(new_move, fieldling.y_dim, fieldling.x_dim)
        if not good_move or good_move in fieldling.visited:
            print "Try again"
        else:
            move_val = raw_input("What goes here? Key in 'f' for flag or 'o' for open ")
            if move_val == 'f' or move_val == 'F':
                fieldling.set_cell(good_move, 'F')
                print fieldling
            elif move_val == 'o' or move_val == 'O':
                mine = fieldling.is_mine(good_move)
                print "closed cells:", fieldling.closed
                if mine:
                    print "Bang bang"
                    print fieldling.get_mat()
                    exit()
                print fieldling
            else:
                print "Come again"
    else:
        print "You win"
        print fieldling


def is_valid_move(move, height, width):
    if move == 'b':
        print 'bye'
        exit()
    move = move.strip().split()
    if len(move) != 2:
        return False
    try:
        move = map(int, move)
        vert, hor = move
        if 0 <= vert < height and 0 <= hor < width:
            return vert, hor
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    make_subsequent_moves(make_first_move(start_game()))
    # new_field = Field(9, 9, 10)
    # print new_field.get_mat()
    # print new_field
    # # print new_field[0][0]
    # new_field.is_mine((8, 0))
    # print new_field
