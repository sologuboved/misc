import re


def add_cd(source_fname, res_fname):
    with open(source_fname, 'r') as source_handler, open(res_fname, 'w') as res_handler:
        for line in source_handler.readlines():
            res_handler.write('cd ../{}/\n'.format(re.findall(r':.+?/(.+?).git', line)[0]))
            res_handler.write(line)


if __name__ == '__main__':
    add_cd('git_comms_source.txt', 'git_comms.txt')
