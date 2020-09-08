from datetime import date


def count_portion(beg_date, fin_date, beg_item, fin_item, per_day=5, initial_amount=None):
    res = (fin_item - beg_item - (fin_date - beg_date).days * per_day) / per_day
    if initial_amount:
        print(initial_amount + res)
    else:
        print(res)


if __name__ == '__main__':
    count_portion(date(2020, 9, 3), date(2020, 9, 8), 250, 490, initial_amount=337)
