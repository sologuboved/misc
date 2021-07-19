def add_paragraphs():
    with open('post.txt') as handler:
        lines = handler.readlines()
    with open('post.txt', 'w') as handler:
        for line in lines:
            line = line.strip()
            if line:
                handler.write(f'<p>{line}</p>\n')


if __name__ == '__main__':
    add_paragraphs()
