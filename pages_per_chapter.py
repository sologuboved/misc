def count_pages(pages):
    count = dict()
    start = pages[0]
    next_index = 1
    while next_index < len(pages):
        finish = pages[next_index]
        if start == finish:
            next_index += 1
            continue
        count[start] = finish - start
        start = finish
        next_index += 1
    return count


def fill_in_zeros(num):
    num = str(num)
    return num + ':' + ' ' * (10 - len(num))


def prettyprint_count(pages, val=False):
    count = count_pages(pages).items()
    if val:
        index = 1
    else:
        index = 0
    count.sort(key=lambda p: p[index])
    for page, length in count:
        print "%s %d" % (fill_in_zeros(page), length)


if __name__ == '__main__':
    tr_tr = (15, 22, 32, 42, 55, 61, 75, 87, 98, 110, 118, 135, 149, 159, 169, 181, 195, 206, 218, 229, 259, 278, 298,
             323, 339, 355, 367, 385, 400, 419, 432, 443, 455, 463, 473, 480, 491, 501, 516, 531)
    m_d = (17, 21, 24, 37, 40, 42, 44, 47, 49, 57, 60, 61, 63, 67, 69, 71, 83, 88, 91, 94, 96, 99, 102, 103, 107, 108,
           110, 114, 117, 119, 120, 122, 133, 135, 140, 145, 152, 153, 154, 155, 161, 169, 176, 177, 181, 189, 191, 193,
           202, 203, 206, 209, 211, 214, 231, 235, 238, 240, 243, 245, 248, 252, 253, 254, 261, 263, 264, 266, 268, 269,
           271, 276, 280, 285, 288, 291, 293, 294, 298, 300, 302, 311, 313, 315, 317, 321, 325, 335, 338, 341, 344, 349,
           351, 355, 358, 359)
    prettyprint_count(m_d, True)


