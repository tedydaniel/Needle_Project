import csv
import nltk
from nltk.stem.snowball import EnglishStemmer
import numpy as np


class EstimateLikelihood():


    def __init__(self):
        self.null = {}
        self.all_dates = {}
        self.total = 0
        self.create_null_hypotesis()


    def create_null_hypotesis(self):
        file = open("data\\RedditNews.csv")
        reader = csv.reader(file)
        stops = nltk.corpus.stopwords.words('english')
        next(reader)
        sw_tok = EnglishStemmer()
        for line in reader:
            tokens = [sw_tok.stem(x) for x in nltk.RegexpTokenizer(r'\w\w+|U S').tokenize(line[1])]
            self.all_dates[line[0]] = [x for x in tokens if x not in stops]
            for word in self.all_dates[line[0]]:
                if word in self.null.keys():
                    self.null[word] += 1
                else:
                    self.null[word] = 1
                self.total += 1


    def log_likelihood_by_date(self, date):
        srt = sorted(self.all_dates.keys())
        if date not in srt:
            print("The date is not exist")
            return
        indx = srt.index(date)
        tokens = []
        for i in range(6):
            tokens += self.all_dates[srt[indx - i]]
        local_count = {}
        for word in tokens:
            if word in local_count.keys():
                local_count[word] += 1
            else:
                local_count[word] = 1
        llrs = {}
        for word in tokens:
            llrs[word] = np.log(local_count[word] / self.null[word])
        print(llrs)








es = EstimateLikelihood()
es.log_likelihood_by_date("2011-11-28")




