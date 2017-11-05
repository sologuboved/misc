from matplotlib import pyplot

PERS = {2013: [(1, 4), (27, 4), (23, 5), (17, 6), (13, 7), (13, 8), (9, 9), (5, 10), (30, 10), (26, 11), (23, 12)],
        2014: [(17, 1), (11, 2), (9, 3), (4, 4), (30, 4), (25, 5), (19, 6), (13, 7), (8, 8), (4, 9), (1, 10), (27, 10),
               (22, 11), (18, 12)],
        2015: [(13, 1), (9, 2), (8, 3), (2, 4), (29, 4), (24, 5), (18, 6), (12, 7), (9, 8), (3, 9), (30, 9), (26, 10),
               (21, 11), (18, 12)],
        2016: [(13, 1), (8, 2), (3, 3), (30, 3), (24, 4), (20, 5), (17, 6), (12, 7), (7, 8), (3, 9), (28, 9)]}

LEAPS = {2016}


def get_month_len(month, year):
    if month == 2:
        if year in LEAPS:
            return 29
        else:
            return 28
    if month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    else:
        return 30


def get_yeared():
    return [(date[0], date[1], year) for year in sorted(PERS.keys()) for date in PERS[year]]


def count_length(beg, end):
    beg_day, beg_month, beg_year = beg
    end_day, end_month, end_year = end

    if end_month == beg_month:
        return end_day - beg_day + 1

    duration = get_month_len(beg_month, beg_year) - beg_day + 1
    if beg_year != end_year:
        assert end_year - beg_year == 1, "wrong years: %r and %r" % (beg_year, end_year)
        for month in range(beg_month + 1, 13):
            duration += get_month_len(month, beg_year)
        for month in range(1, end_month):
            duration += get_month_len(month, end_year)
    elif end_month - beg_month != 1:
        for month in range(beg_month + 1, end_month):
            duration += get_month_len(month, beg_year)
    return duration + end_day


def get_all_pers():
    yeared = get_yeared()
    indx = 0
    all_pers = list()
    while indx + 1 < len(yeared):
        beg, end = yeared[indx], yeared[indx + 1]
        length = count_length(beg, end)
        all_pers.append((end, length))
        print beg, 'to', end
        print length
        print
        indx += 1
    return all_pers


def get_next_month_and_year(curr_month, curr_year):
    next_month = curr_month + 1
    if next_month > 12:
        next_month = 1
        next_year = curr_year + 1
    else:
        next_year = curr_year
    return next_month, next_year


def count_next(prev, diap=(25, 28)):
    day, month, year = prev

    for duration in range(diap[0], diap[1] + 1):
        print
        print str(duration) + ':'

        till_end = get_month_len(month, year) - day + 1
        remainder = duration - till_end

        if remainder < 0:
            print (day + duration, month, year)
            continue

        next_month, next_year = get_next_month_and_year(month, year)
        next_len = get_month_len(next_month, next_year)

        while remainder > next_len:
            remainder -= next_len
            next_month, next_year = get_next_month_and_year(next_month, next_year)
            next_len = get_month_len(next_month, next_year)
        print (remainder, next_month, next_year)


def process_pers(all_pers):
    lengths = [item[1] for item in all_pers]
    aver = sum(lengths) / float(len(lengths))
    shortest_date = longest_date = None
    shortest_per = float('inf')
    longest_per = 0
    for per in all_pers:
        length = per[1]
        if length <= shortest_per:
            shortest_per = length
            shortest_date = per[0]
        if length >= longest_per:
            longest_per = length
            longest_date = per[0]
    print "Average period is", aver, "days long"
    print "Shortest period was", shortest_per, "days long, at", '{0}.{1}.{2}'.format(str(shortest_date[0]),
                                                                                     str(shortest_date[1]),
                                                                                     str(shortest_date[2]))
    print "Longest period was", longest_per, "days long, at", '{0}.{1}.{2}'.format(str(longest_date[0]),
                                                                                   str(longest_date[1]),
                                                                                   str(longest_date[2]))


def plot_pers(all_pers):
    y_vals = [item[1] for item in all_pers]
    x_vals = range(len(y_vals))
    pyplot.figure()
    pyplot.plot(x_vals, y_vals, 'o')
    pyplot.show()


if __name__ == '__main__':
    # count_next((28, 9, 2016))
    # print get_all_pers()
    # process_pers(get_all_pers())
    # print count_length((3, 9, 2016), (28, 9, 2016))
    pers = get_all_pers()
    process_pers(pers)
    # plot_pers(pers)
