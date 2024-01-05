from collections import defaultdict

import requests

from global_vars import HEADERS
from helpers import CsvWriter, dump_utf_json, read_csv, which_watch


class Urlage:
    def __init__(self, src='collection.csv'):
        print(f"Processing {src}...")
        self.aberrant_codes = defaultdict(list)
        self.code200 = list()
        self.src = list(read_csv(src, as_dict=True, delimiter=';'))

    def process(self):
        total = len(self.src)
        count = 0
        for row in self.src:
            count += 1
            if count == 1 or count == total or not count % 10:
                print(f"{count} / {total}")
            try:
                response = requests.get(row['url'], headers=HEADERS)
            except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ConnectTimeout,
                    requests.exceptions.ReadTimeout,
            ) as e:
                self.aberrant_codes[str(e)].append(row)
            else:
                code = response.status_code
                if code == 200:
                    title = row['title']
                    if (not title) or title[:20] in response.text:
                        self.code200.append(row)
                    else:
                        self.aberrant_codes["title_not_found"].append(row)
                else:
                    self.aberrant_codes[str(code)].append(row)

    @which_watch
    def main(self):
        try:
            self.process()
        except BaseException:
            raise
        finally:
            dump_utf_json(self.aberrant_codes, 'collection_aberrant.json')
            with CsvWriter(
                    'collection_old.csv',
                    headers=('url', 'title', 'author', 'pairing', 'translator', 'comment', 'fandom'),
                    as_dict=True,
            ) as handler:
                handler.bulk(self.code200)


if __name__ == '__main__':
    Urlage().main()
