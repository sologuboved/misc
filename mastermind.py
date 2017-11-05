import itertools
import random
from sys import exit


class Game(object):
    def __init__(self, num_items, num_colors):
        self._num_items = num_items
        self._num_colors = num_colors
        self.poss_arrangements = self.get_poss_arrangements()

    def get_poss_arrangements(self):
        elements = [element for element in range(self._num_colors)]
        poss_combs = itertools.combinations_with_replacement(elements, self._num_items)
        poss_arrangements = set()
        for comb in poss_combs:
            poss_arrangements.update(set(itertools.permutations(comb)))
        return poss_arrangements

    def get_scores(self, actual_arrangement, prospective_arrangement):
        assert len(actual_arrangement) == len(prospective_arrangement), "get_scores: Lengths mismatch"
        second_score = self.get_raw_second_score(list(actual_arrangement), list(prospective_arrangement), 0)
        first_score = 0
        for ind in range(self._num_items):
            if actual_arrangement[ind] == prospective_arrangement[ind]:
                first_score += 1
        second_score = second_score - first_score
        return first_score, second_score

    def get_raw_second_score(self, actual_arrangement, prospective_arrangement, second_score):
        if not (actual_arrangement and prospective_arrangement):
            return second_score

        for ind in range(len(actual_arrangement)):
            element = actual_arrangement[ind]
            if element in prospective_arrangement:
                second_score += 1
                if ind + 1 < len(actual_arrangement):
                    actual_arrangement = actual_arrangement[ind + 1:]
                    prospective_arrangement.remove(element)
                    return self.get_raw_second_score(actual_arrangement, prospective_arrangement, second_score)
                return second_score

        return second_score

    def arrangement_matches(self, actual_arrangement, prospective_arrangement, scores):
        return scores == self.get_scores(actual_arrangement, prospective_arrangement)

    def update_poss_arrangements(self, actual_arrangement, scores):
        updated_arrangements = set()
        for prospective_arrangement in self.poss_arrangements:
            if self.arrangement_matches(actual_arrangement, prospective_arrangement, scores):
                updated_arrangements.add(prospective_arrangement)
        print "Updated arrangements:", updated_arrangements
        print
        self.poss_arrangements = updated_arrangements

    def evaluate_score(self):
        while True:
            score = raw_input("Evaluate or q for quit: ")
            if score == 'q':
                return False
            try:
                first, second = map(int, score.split())
                print "right color right position:", first
                print "right color wrong position:", second
                confirmation = raw_input("Alright? y for yes: ")
                if confirmation == 'y':
                    return first, second
            except:
                print "Wrong, try again"

    def play_simplest(self):
        while self.poss_arrangements:
            arrangement = self.poss_arrangements.pop()
            print "New arrangement:", arrangement
            scores = self.evaluate_score()
            if not scores:
                print 'Bye'
                exit()
            if scores == (self._num_items, 0):
                print "Grats"
                exit()
            self.update_poss_arrangements(arrangement, scores)
        print "Something went wrong: No arrangements left"

    def play(self, start=None):
        first_iter = True
        while self.poss_arrangements:
            if not first_iter:
                arrangement = self.poss_arrangements.pop()
            else:
                if start:
                    arrangement = start
                else:
                    arrangement = tuple([random.choice(range(self._num_colors)) for _ in range(self._num_items)])
                first_iter = False
            print "New arrangement:", arrangement
            scores = self.evaluate_score()
            if not scores:
                print 'Bye'
                exit()
            if scores == (self._num_items, 0):
                print "Grats"
                exit()
            self.update_poss_arrangements(arrangement, scores)
        print "Something went wrong: No arrangements left"

    def autoplay(self, mode):
        """
        0: pop()
        1: random
        tuple: pregiven
        """
        target = tuple([random.choice(range(self._num_colors)) for _ in range(self._num_items)])
        print 'Target:', target
        attempts = 0
        first_iter = True
        while self.poss_arrangements:
            if first_iter:
                first_iter = False
                if mode == 0:
                    arrangement = self.poss_arrangements.pop()
                elif mode == 1:
                    arrangement = tuple([random.choice(range(self._num_colors)) for _ in range(self._num_items)])
                elif mode in self.poss_arrangements:
                    arrangement = mode
                else:
                    print "Wrong mode:", mode
                    quit()
            else:
                arrangement = self.poss_arrangements.pop()
            print "New arrangement:", arrangement
            attempts += 1
            print 'Attempts:', attempts
            scores = self.get_scores(arrangement, target)
            print 'Scores:', scores
            if scores == (self._num_items, 0):
                return attempts
            self.update_poss_arrangements(arrangement, scores)
        print "Something went wrong: No arrangements left"

    def consult(self, scored_arrangements):
        for arrangement in scored_arrangements:
            self.update_poss_arrangements(arrangement, scored_arrangements[arrangement])
        print self.poss_arrangements

    def consult_interactively(self):
        while self.poss_arrangements:
            print self.poss_arrangements
            arrangement = raw_input("Arrangement or 'q' for quit: ")
            scores = raw_input("Score or 'q' for quit: ")
            if arrangement == 'q' or scores == 'q':
                print 'Bye'
                return
            print "Arrangement is", arrangement
            print "Score is", scores
            confirmation = raw_input("Is this correct? ")
            if confirmation == 'y':
                try:
                    arrangement = tuple([int(char) for char in arrangement])
                    scores = tuple(map(int, scores.split()))
                except:
                    print "Wrong, try again!"
                    continue
                if len(arrangement) != self._num_items or len(scores) != 2:
                    print "Wrong, try again!"
                    continue
                if scores == (self._num_items, 0):
                    print 'Grats'
                    exit()
                self.update_poss_arrangements(arrangement, scores)
            else:
                continue
        else:
            print "No arrangements left"


def test_scoring(only_raw_second=False):
    samples = [[[1, 1, 1, 1], [2, 2, 1, 2], 1, (1, 0)],
               [[1, 2, 3, 4], [4, 3, 2, 1], 4, (0, 4)],
               [[2, 2, 3, 3], [1, 3, 4, 2], 2, (0, 2)],
               [[1, 3, 3, 3], [1, 2, 2, 2], 1, (1, 0)],
               [[4, 4, 2, 2], [2, 4, 2, 4], 4, (2, 2)],
               [[2, 2, 4, 4], [4, 2, 3, 3], 2, (1, 1)],
               [[1, 2, 3, 1], [4, 4, 4, 4], 0, (0, 0)],
               [[1, 2, 3, 4], [1, 2, 3, 4], 4, (4, 0)],
               [[1, 2, 3, 4], [1, 3, 3, 4], 3, (3, 0)],
               [[1, 1, 1, 1], [1, 1, 1, 1], 4, (4, 0)]]

    test_res = list()

    if only_raw_second:
        for element in samples:
            actual_arrangement, prospective_arrangement, raw_second, scores = element
            game = Game(4, 4)
            res_raw_second = game.get_raw_second_score(actual_arrangement, prospective_arrangement, 0)
            if res_raw_second != raw_second:
                print actual_arrangement, prospective_arrangement
                print raw_second, res_raw_second
            else:
                test_res.append(True)
        print 'Passed', sum(test_res), "out of", len(samples)
        return

    for element in samples:
        actual_arrangement, prospective_arrangement, raw_second, scores = element
        first, second = scores
        game = Game(4, 4)
        res_first, res_second = game.get_scores(tuple(actual_arrangement), tuple(prospective_arrangement))
        if res_first != first or res_second != second:
            print actual_arrangement, prospective_arrangement
            print first, res_first
            print second, res_second
            print
        else:
            test_res.append(True)
    print 'Passed', sum(test_res), "out of", len(samples)


def find_statistics(num_items=5, num_colors=5, tests=1000):
    start_pop = list()
    start_random = list()
    start_01234 = list()
    start_00000 = list()
    for test in range(tests):
        print '---------------------', test, '---------------------'
        start_pop.append(Game(num_items, num_colors).autoplay(0))
        start_random.append(Game(num_items, num_colors).autoplay(1))
        start_01234.append(Game(num_items, num_colors).autoplay((0, 1, 2, 3, 4)))
        start_00000.append(Game(num_items, num_colors).autoplay((0, 0, 0, 0, 0)))
    print
    print 'Pop:', sum(start_pop) / float(tests), min(start_pop), max(start_pop)
    print 'Random:', sum(start_random) / float(tests), min(start_random), max(start_random)
    print '01234:', sum(start_01234) / float(tests), min(start_01234), max(start_01234)
    print '00000:', sum(start_00000) / float(tests), min(start_00000), max(start_00000)


if __name__ == '__main__':
    # scored = {(0, 1, 2, 3): (0, 3),
    #           (3, 4, 0, 2): (0, 3),
    #           (2, 0, 4, 1): (0, 4)}
    # Game(4, 10).consult(scored)
    # t = (0, 1, 2, 3, 4)
    # Game(4, 10).play()
    # Game(5, 5).autoplay(1)
    # find_statistics(tests=10000)
    Game(4, 10).consult_interactively()
