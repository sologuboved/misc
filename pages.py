BEGINNING = 116
END = 360
DAYS = 90
PAGES = 2


def count_variants(beg, end, days, pages):
    to_read = end - beg
    for interim in reversed(range(0, days, 5)):
        print(interim, days - interim, float(to_read - interim * pages) / (days - interim))


if __name__ == '__main__':
    count_variants(BEGINNING, END, DAYS, PAGES)
