import re
import json
from collections import defaultdict


class PrereformSpellchecker:
    def __init__(self, filename, dump=None):
        self.filename = filename
        self.dump = dump
        handler = open(self.filename, 'rt')
        self.contents = handler.read()
        handler.close()
        self.report = defaultdict(int)

    def launch(self):
        self.traverse_words()
        with open(self.filename, 'wt') as handler:
            handler.write(self.contents)
        self.deliver_report()

    def traverse_words(self):
        for raw_word in re.findall(r'\b(\S+?)\b|\s', self.contents):
            if raw_word:
                word = correct_word(raw_word)
                if word != raw_word:
                    self.contents = self.contents.replace(raw_word, word)
                    self.report['{} -> {}'.format(raw_word, word)] += 1

    def deliver_report(self):
        print("{} separate instance(s), {} fix(es)".format(len(self.report), sum(self.report.values())))
        if self.report:
            if self.dump:
                with open(self.dump, 'w', encoding='utf-8') as handler:
                    json.dump(self.report, handler, ensure_ascii=False, sort_keys=True, indent=2)
            else:
                for fix in self.report:
                    print(fix)


def correct_word(raw_word):
    word = re.sub(r'(и)(?=[аеёиоуыэюя])', i_fixer, raw_word, flags=re.IGNORECASE)
    if word[-1] in 'бвгджзклмнпрстфхцчщщ':
        word += 'ъ'
    return word


def i_fixer(matchobj):
    if matchobj.group(1).isupper():
        return 'І'
    else:
        return 'і'


if __name__ == '__main__':
    PrereformSpellchecker('post.txt').launch()
