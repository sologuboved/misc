import os
import re


def get_line(foldername, scriptname):
    return "* * * * * /home/askibinskaya/venv_py3/bin/python " \
           "/home/askibinskaya/scripts/{foldername}/{scriptname}.py > " \
           "/home/askibinskaya/scripts/{foldername}/{scriptname}.log 2> " \
           "/home/askibinskaya/scripts/{foldername}/{scriptname}.err".format(foldername=foldername,
                                                                             scriptname=scriptname)


def get_lines(filename, *args):
    lines = '\n'.join([get_line(foldername, scriptname) for foldername, scriptname in args])
    print(lines)
    with open(filename, 'wt') as handler:
        handler.write(lines)


def collect_fnames(path, sieve):
    return [str(filename).rsplit('.', 1)[0] for filename in filter(sieve, os.listdir(path))]


if __name__ == '__main__':
    get_lines('/Users/sologuboved/InfoCulture/datacollector/crontab_lines.txt',
              *[('datacollector', fname) for fname in collect_fnames('/Users/sologuboved/InfoCulture/datacollector',
                                                                     lambda x: re.match(r'^updater_.+?\.py$',
                                                                                        x,
                                                                                        flags=re.IGNORECASE))])
