import calendar
import datetime
from math import ceil


def find_date(total, per_day, weekdays, excl, start=None):
    if start:
        day = datetime.date(*reversed(list(map(lambda x: int(x), start.split('.')))))
    else:
        day = datetime.date.today()
    if weekdays:
        if excl:
            weekdays = [weekday for weekday in range(7) if weekday not in weekdays]
    num_days = int(ceil(total / per_day))
    while num_days:
        if not weekdays or calendar.weekday(day.year, day.month, day.day) in weekdays:
            num_days -= 1
        day += datetime.timedelta(1)
    fin = day - datetime.timedelta(1)
    return fin.strftime("%A, %d %B %Y")


if __name__ == '__main__':
    print(find_date(223, 1, (5, 6), True))
