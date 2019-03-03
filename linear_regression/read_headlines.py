import csv
import re
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
words_sum = {}


def date_to_int(date_string):
    return int(re.sub(r'-', '', date_string))


def headline_to_words(text):
    replaced = re.sub(r'[^A-Za-z -]', '', text)
    replaced = re.sub(r'[-\s]+', ' ', replaced).lower()
    return lemmatizer.lemmatize(replaced).split(" ")


def filter_stop_words(array, new_words_array):
    for word in new_words_array:
        if len(word) and word not in stop_words:
            if word in words_sum:
                words_sum[word] += 1
            else:
                words_sum[word] = 1
            array.append(word)


def read():
    headlines = {}
    with open('../data/reddit.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        last_date = ""
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            if row[1] != last_date:
                last_date = row[1]
                headlines[row[1]] = []
            filter_stop_words(headlines[row[1]], headline_to_words(row[4]))

    frequent_words_sum = {k: v for k, v in words_sum.items() if v > 3000}
    frequent_words = list(frequent_words_sum.keys())
    frequent_words_nums = list(frequent_words_sum.values())
    index_vec = np.arange(len(frequent_words))
    if __name__ == "__main__":
        print(len(frequent_words))

    words_vecs = {}
    for key, v in headlines.items():
        counter = np.vectorize(lambda x: v.count(frequent_words[x]))
        words_vecs[date_to_int(key)] = counter(index_vec)

    return words_vecs, frequent_words, frequent_words_nums


if __name__ == "__main__":
    h, k1, f = read()
    print(k1, f)
    j = 0
    for key1 in h:
        j += 1
        if j > 100:
            break
        else:
            print(key1, h[key1])
