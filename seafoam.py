import random
from sys import exit


class Player(object):
    def __init__(self):
        self.field = [['0' for cell in range(10)] for line in range(10)]
        self.imaginary_enemy_field = [['0' for cell in range(10)] for line in range(10)]
        self.real_enemy_field = None
        self.list_of_possible_coordinates = [(x, y) for x in range(10) for y in range(10)]
        self.list_of_ships = []
        self.list_of_enemy_ships = []
        self.sinking_ship = []  # here go the coordinates of the cells of the ship Computer has hit as they are hit
        self.exhibits = set()  # here go the coordinates of the cells that have already been checked

    def get_field_pic(self, field):
        # prints the field as a grid
        field_pic = ''
        for line in field:
            for cell in line:
                field_pic += cell + ' '
            else:
                field_pic += '\n'
        return field_pic

    def are_coordinates_valid(self, field, x, y, sinking=False):
        # checks is the cell in question has common borders or corners with ships
        lab = set()
        if x in range(len(field)) and y in range(len(field)):
            for around in range(-1, 2):
                test_x = x + around
                for about in range(-1, 2):
                    test_y = y + about
                    lab.add((test_x, test_y))
            lab.difference_update(self.exhibits)
            self.exhibits.update(lab)
            for unit in lab:
                if unit[0] in range(len(field)) and unit[1] in range(len(field)):
                    if sinking and [unit[0], unit[1]] not in self.sinking_ship:
                        if field[unit[1]][unit[0]] == 'x':
                            return False
                    else:
                        if field[unit[1]][unit[0]] == '-':
                            return False
            else:
                return True
        else:
            return False

    def establish_subsequent_coordinates(self, field, length, direction, x, y):
        # builds new cells of ships, starting with the given coordinates, with the given length and direction 
        ploio = []
        v, w = x, y
        for i in range(length - 1):
            v, w = self.find_new_coordinates_for_check(direction, v, w)
            if not self.are_coordinates_valid(field, v, w):
                return False
            ploio.append((v, w))
        else:
            self.exhibits = set()
            ploio.append((x, y))
            ploio.sort()
        for (x, y) in ploio:
            field[y][x] = '-'
        self.list_of_ships.append(ploio)
        return True

    def find_new_coordinates_for_check(self, direction, x, y):
        # provides coordinates for check_subsequent_coordinates function
        if direction == 0:  # right
            x += 1
        elif direction == 1:  # down
            y += 1
        elif direction == 2:  # left
            x -= 1
        elif direction == 3:  # up
            y -= 1
        else:
            print "Something went wrong with the direction\n"
        return x, y

    def check_shot(self, coords):
        # checks what is there in the given cell at the enemy's field and returns the result
        if tuple(coords) in self.list_of_possible_coordinates:
            self.list_of_possible_coordinates.remove(tuple(coords))
        if self.real_enemy_field[coords[1]][coords[0]] == 'x' or self.real_enemy_field[coords[1]][coords[0]] == '.':
            return 'again'
        else:
            for ship in self.list_of_enemy_ships:
                if tuple(coords) in ship:
                    if len(ship) == 1:
                        self.list_of_enemy_ships.remove(ship)
                        self.imaginary_enemy_field[coords[1]][coords[0]] = 'x'
                        self.real_enemy_field[coords[1]][coords[0]] = 'x'
                        return 'sunk'
                    else:
                        del ship[ship.index(tuple(coords))]
                        self.imaginary_enemy_field[coords[1]][coords[0]] = 'x'
                        self.real_enemy_field[coords[1]][coords[0]] = 'x'
                        return 'hit'
            else:
                self.imaginary_enemy_field[coords[1]][coords[0]] = '.'
                self.real_enemy_field[coords[1]][coords[0]] = '.'
                return 'missed'


class Computer(Player):
    def __init__(self):
        super(Computer, self).__init__()
        self.mayhem = []

    def establish_length(self):
        # establishes which type of ship to start building and launches building
        squares = 4
        ships = 1
        while squares > 0:
            for el in range(ships):
                self.establish_starting_coordinate(squares)
            else:
                squares, ships = squares - 1, ships + 1

    def establish_starting_coordinate(self, length):
        # picks new starting coordinates and direction until the the ship fits
        while True:
            direction = random.randrange(2)
            coord1 = random.randrange(len(self.field))
            coord2 = random.randrange(len(self.field))
            if not self.are_coordinates_valid(self.field, coord1, coord2):
                self.exhibits = set()
                continue
            if self.establish_subsequent_coordinates(self.field, length, direction, coord1, coord2):
                self.exhibits = set()
                break

    def create_mayhem(self, shot, first_phase=True):
        # after Computer hits a >1-cell ship, creates a list if cells where it makes sense to shoot next
        if first_phase:
            self.mayhem = [[shot[0], shot[1] - 1],
                           [shot[0] + 1, shot[1]],
                           [shot[0], shot[1] + 1],
                           [shot[0] - 1, shot[1]]]
        else:
            x_comparison = []
            y_comparison = []
            for cell in self.sinking_ship:
                x_comparison.append(cell[0])
                y_comparison.append(cell[1])
            x_top = max(x_comparison)
            x_bottom = min(x_comparison)
            y_top = max(y_comparison)
            y_bottom = min(y_comparison)
            if x_top != x_bottom:
                self.mayhem = [[x_top + 1, y_top], [x_bottom - 1, y_top]]
            elif y_top != y_bottom:
                self.mayhem = [[x_top, y_top + 1], [x_top, y_bottom - 1]]
            else:
                print "Something went wrong with the mayhem\n"

        mayhem_copy = self.mayhem[:]
        for coords in mayhem_copy:
            if (tuple(coords) in self.list_of_possible_coordinates and not self.are_coordinates_valid(
                    self.imaginary_enemy_field, coords[0], coords[1], True)) \
                    or tuple(coords) not in self.list_of_possible_coordinates:
                self.mayhem.remove(coords)
        self.exhibits = set()

    def get_shot(self):
        # Computer shoots
        if len(self.mayhem) > 0:
            choice = self.mayhem[0]
            print "Computer shoots at", (choice[0] + 1, choice[1] + 1)
            shot = self.check_shot(choice)
            if shot == 'missed':
                print "Computer missed\n"
                del self.mayhem[0]
            elif shot == 'hit':
                print "Computer hit your vessel\n"
                self.sinking_ship.append(list(choice))
                self.create_mayhem(list(choice), False)
            elif shot == 'sunk':
                print "Computer sank your vessel\n"
                self.mayhem = []
                self.sinking_ship = []
            else:
                print "Something went wrong with Computer's shot-2\n"
        else:
            choice = self.list_of_possible_coordinates[random.randrange(len(self.list_of_possible_coordinates))]
            print "Computer shoots at", (choice[0] + 1, choice[1] + 1)
            shot = self.check_shot(choice)
            if shot == 'missed':
                print "Computer missed\n"
            elif shot == 'hit':
                print "Computer hit your vessel\n"
                self.sinking_ship.append(list(choice))
                self.create_mayhem(list(choice))
            elif shot == 'sunk':
                print "Computer sank your vessel\n"
            else:
                print "Something went wrong with Computer's shot-1\n"
                exit()
        return shot


class Human(Player):
    def __init__(self):
        super(Human, self).__init__()

    def get_start_coords(self):
        """establishes the number and type of ships to be built by Human 
        and prompts her to provide the starting coordinates for each"""
        squares = 4
        ships = 1
        count = 0
        choice = None
        while squares > 0:
            for el in range(ships):
                if choice != 'e':
                    print "\nLet's settle your %r-square vessel. This is your field:\n" % squares
                    print self.get_field_pic(self.field)
                    while True:
                        choice = raw_input("Key in X, Y (space separated) in range [1, 10] or 'e' for 'enough': ")
                        if choice == 'e':
                            print "\nAlright, no more ships of yours\n"
                            break
                        else:
                            if len(self.process_input(choice)) > 0:
                                coord1 = self.process_input(choice)[0]
                                coord2 = self.process_input(choice)[1]
                                if count < 6:
                                    direction = self.get_direction()
                                else:
                                    direction = 0
                                if not self.are_coordinates_valid(self.field, coord1, coord2):
                                    print "\nAnother vessel or the field border is in the way\n"
                                    self.exhibits = set()
                                    continue
                                if self.establish_subsequent_coordinates(self.field, squares, direction, coord1,
                                                                         coord2):
                                    break
                                else:
                                    print "\nAnother vessel or the field border is in the way\n"
                            else:
                                print "\nHas to be two numbers within range, space separated\n"
                    count += 1
                else:
                    squares = 0
                    break
            else:
                squares, ships = squares - 1, ships + 1

    def get_direction(self):
        # prompts Human to provide direction in which the new cells should be built
        while True:
            direction = raw_input(
                "Choose direction by typing in 'r' for right, 'l' for left, 'd' for downward, or 'u' for upward ")
            if direction == 'r':
                return 0
            elif direction == 'd':
                return 1
            elif direction == 'l':
                return 2
            elif direction == 'u':
                return 3
            else:
                print "'r', 'l', 'd', or 'u'?"

    def process_input(self, inp):
        # turns Human's input into a list of proper coordinates
        processed = []
        if len(inp.split()) == 2:
            for el in inp.split():
                if self.validate_input(el):
                    processed.append(int(el) - 1)
                else:
                    processed = []
                    break
        return processed

    def validate_input(self, coord):
        # checks if the coordinate is within the field length
        try:
            coord = int(coord)
            return coord in range(1, len(self.field) + 1)
        except:
            return False

    def get_shot(self):
        # prompts Human to shoot
        while True:
            shot = raw_input(
                "\nYou shoot. Key in X, Y (space separated) within range between 1 and 10 or 'i' for 'interrupt game': ")
            if shot == 'i':
                print "\nComputer's field:\n", self.get_field_pic(self.real_enemy_field)
                print 'Goodbye'
                exit()
            shot = self.process_input(shot)
            if len(shot) > 0:
                result = self.check_shot(shot)
                if result == 'again':
                    print "You've been there, try again\n"
                elif result == 'missed':
                    self.imaginary_enemy_field[shot[1]][shot[0]] = '.'
                    print "You missed\n"
                elif result == 'hit':
                    self.imaginary_enemy_field[shot[1]][shot[0]] = 'x'
                    print "You hit"
                elif result == 'sunk':
                    self.imaginary_enemy_field[shot[1]][shot[0]] = 'x'
                    print "You sank a ship\n"
                else:
                    print "Something went wrong with the return\n"
                return result
            else:
                print "Has to be two numbers within range, space separated\n"


class Game(object):
    def __init__(self):
        self.comp = Computer()
        self.user = Human()

    def set_ships(self):
        self.comp.establish_length()
        self.user.real_enemy_field = list(self.comp.field)
        self.user.list_of_enemy_ships = self.comp.list_of_ships
        self.user.get_start_coords()
        self.comp.real_enemy_field = list(self.user.field)
        self.comp.list_of_enemy_ships = self.user.list_of_ships
        print "\nYour field:\n", self.comp.get_field_pic(self.comp.real_enemy_field)
        print "\nComputer's field:\n", self.user.get_field_pic(self.user.imaginary_enemy_field)

    def turn_coefficient(self, which):
        if which == 'missed':
            return -1
        else:
            return 1

    def take_turns(self):
        turn = 1
        while len(self.comp.list_of_ships) > 0 and len(self.user.list_of_ships) > 0:
            if turn > 0:
                # print '\n', self.user.list_of_enemy_ships # beware the coordinates in this list are in range(10)
                result = self.user.get_shot()
                print "Computer's field:\n", self.user.get_field_pic(self.user.imaginary_enemy_field)
            else:
                result = self.comp.get_shot()
                print "Your field:\n", self.comp.get_field_pic(self.comp.real_enemy_field)
            turn *= self.turn_coefficient(result)
        else:
            if len(self.comp.list_of_ships) > 0:
                print "YOU LOSE\n"
                print "Computer's field:\n", self.user.get_field_pic(self.user.real_enemy_field)
            else:
                print "YOU WIN"
            while True:
                another_round = raw_input("Care for another round? Y, N ")
                if another_round.lower() == 'n':
                    print 'Goodbye'
                    return False
                elif another_round.lower() == 'y':
                    print "Welcome to it"
                    return True
                else:
                    print "That was neither Y nor N"


def new_round():
    on = True
    while on:
        new_game = Game()
        new_game.set_ships()
        on = new_game.take_turns()
    exit()


if __name__ == "__main__":
    new_round()
