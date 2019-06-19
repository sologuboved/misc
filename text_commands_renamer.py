import re


def rename_text_commands(fname):
    fname_pattern = re.compile(r'\s(\w+?)_([a-z]+?)\.')
    with open(fname) as handler:
        text_commands = fname_pattern.sub(r' \2_\1.', handler.read())
    with open(fname, 'w') as handler:
        handler.write(text_commands)


if __name__ == '__main__':
    rename_text_commands('text_commands.txt')
