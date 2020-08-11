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
        for raw_word in re.findall(r'\b(\S+?)\b|\s', self.contents):
            if raw_word:
                word = correct_word(raw_word)
                if word != raw_word:
                    self.contents = self.contents.replace(raw_word, word)
                    self.report['{} -> {}'.format(raw_word, word)] += 1

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
    word = re.sub(r'(и)(?=[аеёиоуыэюя])', i_fixer, raw_word, flags=re.IGNORECASE)
    if word.lower() not in ('др', 'проч', 'т', 'д', 'п') and word[-1] in 'бвгджзклмнпрстфхцчшщ':
        word += 'ъ'
    return word


def i_fixer(matchobj):
    if matchobj.group(1).isupper():
        return 'І'
    else:
        return 'і'


if __name__ == '__main__':
    PrereformSpellchecker('post.txt').launch()
