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
