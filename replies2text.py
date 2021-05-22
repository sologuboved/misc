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


if __name__ == '__main__':
    turn_to_text('text.txt')
