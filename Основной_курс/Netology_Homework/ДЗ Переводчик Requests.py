import requests
import os
from pathlib import Path

API_KEY = 'trnsl.1.1.20190710T193723Z.888dd0a4855f0803.39a554a6cff475e91a0e9615eabbd5a23e057af0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate_it(file_path, result_file_path, from_lang, to_lang):
    file_name = Path(file_path)
    with open(file_name, 'r', encoding='UTF-8') as text:
        params = {'key': API_KEY, 'text': text, 'lang': '{}-{}'.format(from_lang, to_lang)}
        response = requests.get(URL, params=params)
        json_ = response.json()
        print(''.join(json_['text']))
        new_file = os.path.join(result_file_path, 'translation_{}.txt'.format(from_lang))
        with open(new_file, 'w+', encoding='UTF-8') as translation:
            translation.write(''.join(json_['text']))


translate_it('C:\\_fforhw\\DE.txt', 'C:\\_fforhw\\res', 'de', 'ru')
translate_it('C:\\_fforhw\\FR.txt', 'C:\\_fforhw\\res', 'fr', 'ru')
translate_it('C:\\_fforhw\\ES.txt', 'C:\\_fforhw\\res', 'es', 'ru')