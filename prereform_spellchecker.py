import re

# def correct(filename):
#     with open(filename) as handler:
#         raw_contents = handler.read()
#         for consonant in 'бвгджзклмнпрстфхцчшщ':
#             raw_contents = raw_contents.replace(consonant + " ", consonant + 'ъ' + " ")
#         for vowel in 'аеёиоуыэюя':
#             raw_contents = raw_contents.replace('и' + vowel, 'і' + vowel)
#         for index in range(len(raw_contents)):
#             pass
#     with open(filename, 'wt') as handler:
#         handler.write(raw_contents)


class PrereformSpellchecker:
    def __init__(self, filename):
        self.filename = filename
        handler = open(self.filename, 'rt')
        self.contents = re.split(r'\s\s*', handler.read())
        handler.close()
        self.report = {'i_count': 0, 'i_fixed': list(), 'ъ_count': 0, 'ъ_replaced': list()}

    def launch(self):
        print(repr(self.contents))
        # with open(self.filename, 'wt') as handler:
        #     handler.write(self.raw_contents)

    def fix_i(self):
        for index in range(len(self.contents)):
            char = self.contents[index]
            if char == 'и':
                try:
                    next_char = self.contents[index + 1]
                except IndexError:
                    break
                if next_char in 'аеёиоуыэюя':
                    self.contents[index] = 'і'
                    self.report['i_count'] += 1

    def get_word(self, index):
        beg = fin = None
        delta = 0
        while True:
            if None not in (beg, fin):
                return self.contents[beg: fin]
            delta += 1
            if self.contents[index - delta] in " \n\t\r\f\v":
                fin = index + delta
            if self.contents[index + delta] in " \n\t\r\f\v":
                fin = index + delta

    def is_beg_or_fin(self, index):
        try:
            char = self.contents[index]
        except IndexError:
            return True
        if char in " \n\t\r\f\v":
            pass





if __name__ == '__main__':
    prereform_spellchecker = PrereformSpellchecker('post.txt')
    prereform_spellchecker.launch()
