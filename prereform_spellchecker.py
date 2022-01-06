import re
import json
from collections import defaultdict

_consonants = 'бвгджзклмнпрстфхцчшщ'


class PrereformSpellchecker:
    def __init__(self, filename, dump_to=None):
        self.filename = filename
        self.dump_to = dump_to
        handler = open(self.filename, 'rt')
        self.contents = handler.read()
        handler.close()
        self.report = defaultdict(int)

    def launch(self):
        self.parse_by_word()
        with open(self.filename, 'wt') as handler:
            handler.write(self.contents)
        self.deliver_report()

    def parse_by_word(self):
        paragraphs = self.contents.split('\n')
        for paragraph_index in range(len(paragraphs)):
            paragraph = paragraphs[paragraph_index]
            words = paragraph.split()
            for index in range(len(words)):
                raw_word = words[index].strip()
                word = correct_word(raw_word)
                if raw_word != word:
                    words[index] = word
                    self.report[f'{raw_word} -> {word}'] += 1
            paragraphs[paragraph_index] = " ".join(words)
        self.contents = '\n'.join(paragraphs)

    def deliver_report(self):
        print("{} separate instance(s), {} fix(es)".format(len(self.report), sum(self.report.values())))
        if self.report:
            if self.dump_to:
                with open(self.dump_to, 'w', encoding='utf-8') as handler:
                    json.dump(self.report, handler, ensure_ascii=False, sort_keys=True, indent=2)
            else:
                for items in self.report.items():
                    print("{}: {}".format(*items))


def correct_word(word):
    punctuation_marks = '.,<>/?;:\'"[]{}!()-_=+\\'
    ending = ''
    while True:
        for punctuation_mark in punctuation_marks:
            if word.endswith(punctuation_mark):
                ending = punctuation_mark + ending
                word = word[:-1]
                if not word:
                    return ending
                break
        else:
            break
    word = re.sub(r'(и)(?=[аеёийоуыэюя])', i_fixer, word, flags=re.IGNORECASE)  # удивленіе
    if len(word) > 1 and word.isupper() and not set(word) - set(_consonants.upper()):  # СССР
        return word + ending
    if ('.' in word  # Б.Ф.[ Поршневъ]
            or word.lower() in ('др', 'проч', 'см', 'жж', 'цит')  # цит.[ по]
            or (ending.startswith('.') and word[0].isupper() and len(word) <= 2)):  # Дж.[ Джейнсъ]
        return word + ending
    word = '-'.join(map(er_fixer, word.split('-')))  # какъ-нибудь
    return word + ending


def i_fixer(matchobj):
    if matchobj.group(1).isupper():
        return 'І'
    else:
        return 'і'


def er_fixer(word):
    if word[-1].lower() in _consonants:
        if word.isupper() and len(word) > 1:  # ВОТЪ
            return word + 'Ъ'
        else:
            return word + 'ъ'
    else:
        return word


if __name__ == '__main__':
    PrereformSpellchecker('post.txt').launch()
