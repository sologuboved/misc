def make_filter(key_fieldpath, raw_filter):
    operators = {'>=': '$gte', '<=': '%lte'}

    try:
        return {key_fieldpath: float(raw_filter)}
    except ValueError:
        pass

    if ',' in raw_filter:
        beg, fin = raw_filter[1: -1].split(", ")
        return {key_fieldpath: {'$gte': float(beg), '$lt': float(fin)}}

    operator, pivot = raw_filter.split()
    return {key_fieldpath: {operators[operator]: float(pivot)}}


def add_paragraphs():
    with open('post.txt') as handler:
        lines = handler.readlines()
    with open('post.txt', 'w') as handler:
        for line in lines:
            line = line.strip()
            if line:
                handler.write(f'<p>{line}</p>\n')


def turn_to_text(filename):
    text = ''
    with open(filename) as handler:
        for line in handler.readlines():
            if not line.endswith('\n'):
                line += '\n'
            if line[-2] in {'?', '!', '.'}:
                ending = " "
            else:
                ending = ". "
            text += line[0].upper() + line[1: -1] + ending
    print(text)
