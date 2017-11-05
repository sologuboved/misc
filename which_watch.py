def count_time(start, add):
    next_day = False
    start_h, start_m, start_s = start
    add_h, add_m, add_s = add
    sec = start_s + add_s
    fin_sec = sec % 60
    mins = start_m + add_m + sec // 60
    fin_m = mins % 60
    fin_hrs = start_h + add_h + mins // 60
    if fin_hrs >= 24:
        fin_hrs -= 24
        next_day = True
    return next_day, fin_hrs, fin_m, fin_sec


if __name__ == '__main__':
    print count_time((21, 39, 0), (18, 46, 0))
