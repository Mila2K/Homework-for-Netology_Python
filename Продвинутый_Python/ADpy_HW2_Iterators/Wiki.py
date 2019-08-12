import requests
import chardet
import json
import os


class WikiIterator:
    def __init__(self, result_file_path):
        self.current = -1
        self.dict = dict()
        self.result_file_path = result_file_path
        self.n = 0
        with open('countries.json', 'rb') as f:
            data = f.read()
            detected_encoding = chardet.detect(data)
            data_to_decode = data.decode(detected_encoding['encoding'])
            self.data_json = json.loads(data_to_decode)

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current == len(self.data_json):
            raise StopIteration
        else:
            search = requests.Session()
            URL = "https://en.wikipedia.org/w/api.php"
            PARAMS_1 = {
                'action': "query",
                'list': "search",
                'srsearch': self.data_json[self.current]['name']['official'],
                'format': "json"
            }
            request_1 = search.get(url=URL, params=PARAMS_1)
            DATA_1 = request_1.json()
            page_id = DATA_1['query']['search'][0]['pageid']
            PARAMS_2 = {
                'action': "query",
                'prop': 'info',
                'pageids': page_id,
                'inprop': 'url',
                'format': "json"
            }
            request_2 = search.get(url=URL, params=PARAMS_2)
            DATA_2 = request_2.json()
            link = DATA_2['query']['pages'][str(page_id)]['canonicalurl']
            print(link)
            self.dict[self.data_json[self.current]['name']['official']] = link

        new_file = os.path.join(self.result_file_path, 'write_countries.txt')
        with open(new_file, 'w+', encoding='UTF-8') as write_countries_txt:
            for key, value in self.dict.items():
                print(key, value)
                str_to_write = str('\n' + key + ':' + value + '\n')
                write_countries_txt.write(str_to_write)
        print(write_countries_txt)


iterator = WikiIterator('C:\\_fforhw\\res')
iterator.__next__()
iterator.__next__()