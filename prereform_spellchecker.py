import re
import json
from collections import defaultdict


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


def correct_word(raw_word):
    abbreviations = ('др', 'проч', 'т.д', 'т.п', 'см', 'жж', 'цит')
    consonants = 'бвгджзклмнпрстфхцчшщ'
    ending = ''
    while True:
        for punctuation_mark in '.,<>/?;:\'"[]{}!()-_=+\\':
            if raw_word.endswith(punctuation_mark):
                ending = punctuation_mark + ending
                raw_word = raw_word[:-1]
                break
        else:
            break
    print(raw_word, ending)
    if re.match(r'[А-ЯІѲ]\.[А-ЯІѲ]', raw_word) or (
            ending.startswith('.') and (
            (raw_word.lower() in abbreviations) or (raw_word.isupper() and len(raw_word) == 1)
                )
    ):
        return raw_word + ending
    raw_word = re.sub(r'(и)(?=[аеёийоуыэюя])', i_fixer, raw_word, flags=re.IGNORECASE)
    if raw_word[-1].lower() in consonants:
        raw_word += 'ъ'
    return raw_word + ending


def i_fixer(matchobj):
    if matchobj.group(1).isupper():
        return 'І'
    else:
        return 'і'


if __name__ == '__main__':
    PrereformSpellchecker('post.txt').launch()
