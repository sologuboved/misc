YEAR = 12
FEBR = 28
USUAL = 30


class DayCounter(object):
    def __init__(self, start, days, current_leap=False, next_leap=False):
        assert days <= 366, "too long a period"
        self.start = start
        self.days = days
        self.current_leap = current_leap
        self.next_leap = next_leap
        self.months = self.get_months()

    def get_months(self):
        months = {1: USUAL + 1, 2: FEBR + self.current_leap}
        half = YEAR / 2
        indx = 2
        while indx <= half:
            days = USUAL + (indx % 2 == 0)
            months[indx + 1] = months[indx + half] = days
            indx += 1
        return months

    def what_day(self):
        day, month = self.start
        end_day, end_month = map(str, self.count_days(day, month, self.days))
        return self.add_leading_zeros(end_day) + '.' + self.add_leading_zeros(end_month)

    def count_days(self, day, month, days):
        if month > YEAR:
            self.months[2] = FEBR + self.next_leap
            month -= YEAR
        in_month = self.months[month]
        date = day + days
        if date <= in_month:
            return date, month
        remaining_days = in_month - day + 1
        days -= remaining_days
        return self.count_days(1, month + 1, days)

    def add_leading_zeros(self, string):
        return '0' * (len(string) < 2) + string


if __name__ == '__main__':
    print DayCounter((29, 9), 60).what_day()
