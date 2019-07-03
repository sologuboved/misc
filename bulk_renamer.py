import os
import re


def rename(path, rule, sieve):
    for filename in filter(sieve, os.listdir(path)):
        os.rename(path + filename, path + rule(filename))


if __name__ == '__main__':
    rename('/Users/sologuboved/Werecoder/scholaki/python_cookbook/',
           lambda x: x[1:],
           lambda x: re.match(r'^s.+\.py$', x, flags=re.IGNORECASE))
