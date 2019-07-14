import json
import chardet


def decompos_json():
    with open('newsafr.json', 'rb') as f:
        data = f.read()
        detected_encoding = chardet.detect(data)
        data_to_decode = data.decode(detected_encoding['encoding'])
        data_json = json.loads(data_to_decode)
        desc = ''
        for item in data_json['rss']['channel']['items']:
            desc += ' ' + item['description'].lower()
        return desc


def count_word(decompos_text):
    text_listed = decompos_text.split(' ')
    word_value = {}
    for word in text_listed:
        if len(word) > 6:
            if word in word_value:
                word_value[word] += 1
            else:
                word_value[word] = 1
    return word_value


def sort_top(word_value):
    sort_list = sorted(word_value.items(), key=lambda word_value_l: word_value_l[1], reverse=True)
    count = 1
    top_10 = {}
    for word in sort_list:
        top_10[count] = word
        count += 1
        if count == 10:
            break
    return top_10


def main():
    top_10 = sort_top(count_word(decompos_json()))
    print('\n10 самых часто встречающихся слов (длиной более 6 символов): \n')
    for value in top_10.values():
        print(value[1], ': ', value[0])


main()
