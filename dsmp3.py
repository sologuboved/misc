import os
import pathlib

import requests


def download():
    count = mp3count = 0
    pathlib.Path('dsmp3s').mkdir(parents=True, exist_ok=True)
    entries = requests.get('https://davidsakoyan.com/ru/open-data/api/opera/').json()
    total = len(entries)
    for entry in entries:
        count += 1
        print(f"({count} / {total}) {entry['title_ru']}")
        for performance in entry['performances']:
            local_audio_file = performance['local_audio_file']
            if local_audio_file:
                title = local_audio_file.rsplit('/', 1)[-1]
                print('\t\t' + title)
                with open(os.path.join('dsmp3s', title), 'wb') as handler:
                    handler.write(requests.get(local_audio_file).content)
                    mp3count += 1
    print('Downloaded:', mp3count)


if __name__ == '__main__':
    download()
