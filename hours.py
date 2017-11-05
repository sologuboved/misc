class Calculator(object):
    def __init__(self):
        self.times = list()
        self.total_hrs = self.total_mns = self.total_scs = 0
        self.result = {'hrs': 0, 'mns': 0, 'scs': 0}

    def processed(self, t):
        t.reverse()
        sign = 1
        if t[-1] == 'd':
            del t[-1]
            sign = -1
        try:
            t = map(int, t)
        except:
            return False
        to_pass = [0, 0, 0]
        ind = 0
        while ind < len(t):
            to_pass[ind] = t[ind]
            ind += 1
        self.modify(sign, to_pass)
        return True

    def modify(self, sign, time):
        seconds = time[0]
        minutes = time[1]
        hours = time[2]
        if sign == -1:
            time.append("- subtracted")
        else:
            time.append("- added")
        self.times.append(time)
        self.total_hrs += hours * sign
        self.total_mns += minutes * sign
        self.total_scs += seconds * sign
        self.result = {'hrs': self.total_hrs + (self.total_mns + self.total_scs // 60) // 60,
                       'mns': (self.total_mns + self.total_scs // 60) % 60,
                       'scs': self.total_scs % 60}

    def print_input(self):
        ind = 1
        for time in self.times:
            print "%d) %d hours %d minutes %d seconds %s" % (ind, time[2], time[1], time[0], time[3])
            ind += 1


def key_in():
    print "Key in seconds, minutes, and hours in the reversed order, space separated."
    print "E.g.: 1 48 17 for 1 hour 48 min 17 sec, or 25 0 for 25 min, or 15 for 15 sec."
    print "Or type 's' for 'stop', 'w' to see what is already there on the list, 'r' for results"
    print "If you need to delete an input, type 'd' and the time as prescribed above;"
    print "e.g. d 25 0"
    new = Calculator()
    while True:
        raw_time = raw_input('> ')
        if raw_time == 's':
            print 'Goodbye'
            break
        elif raw_time == 'w':
            new.print_input()
        elif raw_time == 'r' or new.processed(raw_time.split()):
            print 'Total:', new.result['hrs'], 'hours', new.result['mns'], 'minutes', new.result['scs'], 'seconds'
        else:
            print "Do follow the instructions"

if __name__ == "__main__":
    key_in()
