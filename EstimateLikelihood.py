import csv
import nltk
from nltk.stem.snowball import EnglishStemmer
import numpy as np


class EstimateLikelihood():


    def __init__(self):
        self.null = {}
        self.all_dates = {}
        self.total = 0
        self.alternative = {}
        self.local_total = 0
        self.create_null_hypothesis()


    def create_null_hypothesis(self):
        """
        Creates the null hypothesis assuming that each word occurrence is independent, thus
        the probability to see the word is empirical (relative frequency).
        :return: Only updates the fields of the object
        """
        print("Calculating the null hypothesis...")
        file = open("data\\reddit.csv", encoding="utf8")
        reader = csv.reader(file)
        stops = nltk.corpus.stopwords.words('english')
        next(reader)
        sw_tok = EnglishStemmer()
        for line in reader:
            tokens = [sw_tok.stem(x) for x in nltk.RegexpTokenizer(r'\w\w+|U S').tokenize(line[4])]
            self.all_dates[line[1]] = [x for x in tokens if x not in stops]
            for word in self.all_dates[line[1]]:
                self.alternative[word] = 0
                if word in self.null.keys():
                    self.null[word] += 1
                else:
                    self.null[word] = 1
                self.total += 1
        for word in self.null.keys():
            self.null[word] /= self.total


    def count_words_by_date(self, date):
        """
        This function takes all the words which occurred within headline of some news article and
        calculates its fraction (probability). After that, it calculates the log of the likelihood
        ration between the fractions and the null hypothesis. The fraction should be normalized to the same
        scale of the null hypothesis.
        :param date: The date to calculate the likelihood for
        :return: a dictionary with a log likelihood for each word
        """
        srt = sorted(self.all_dates.keys())
        if date not in srt:
            print("The date is not exist")
            return
        print("Counting for " + date)
        indx = srt.index(date)
        tokens = []
        for i in range(6):
            tokens += self.all_dates[srt[indx - i]]
        for word in tokens:
            self.local_total += 1
            self.alternative[word] += 1


    def count_word_from_list_of_dates(self, dates):
        for date in dates:
            self.count_words_by_date(date)
        for word in self.alternative.keys():
            self.alternative[word] /= self.local_total


    def estimate_event(self, date):
        srt = sorted(self.all_dates.keys())
        if date not in srt:
            print("The date is not exist")
            return
        indx = srt.index(date)
        tokens = []
        for i in range(6):
            tokens += self.all_dates[srt[indx - i]]
        local_count = {}
        local_total = 0
        for word in tokens:
            local_total += 1
            if word in local_count.keys():
                local_count[word] += 1
            else:
                local_count[word] = 1

        # llrs = []
        for word in tokens:
            counter = 0
            for event in self.events_by_words[word]:
                if np.log((np.power(event, local_count[word]) * np.power((1 - event), (local_total - local_count[word]))) /
                                  (np.power(self.null[word], local_count[word]) *
                                    np.power((1 - self.null[word]), (local_total - local_count[word])))) > 0:
                    counter += 1
                else:
                    counter -= 1
            if counter > 0:
                print(word)
                print(date)





es = EstimateLikelihood()
es.count_word_from_list_of_dates(['2005-01-03', '2005-01-04', '2006-01-04', '2007-01-04', '2008-01-04', '2008-01-07', '2008-01-16', '2008-03-24', '2009-01-14', '2009-01-15', '2010-01-04', '2011-01-03', '2011-01-04', '2011-08-05'])
es.estimate_event('2010-01-06')
es.estimate_event('2010-01-07')
es.estimate_event('2010-01-08')
es.estimate_event('2010-01-09')
es.estimate_event('2010-01-10')
es.estimate_event('2011-08-05')
es.estimate_event('2011-08-06')
es.estimate_event('2011-08-07')
es.estimate_event('2011-08-08')
# es.count_words_by_date("2011-01-04")




