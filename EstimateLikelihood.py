import csv
import nltk
from nltk.stem.snowball import EnglishStemmer
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import random
import json
import scipy.stats as stat


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
        start = time.time()
        # file = open("data\\reddit.csv", encoding="utf8")
        # reader = csv.reader(file)
        # stops = nltk.corpus.stopwords.words('english')
        # next(reader)
        # sw_tok = EnglishStemmer()
        # for line in reader:
        #     tokens = [sw_tok.stem(x) for x in nltk.RegexpTokenizer(r'\w\w+|U S').tokenize(line[4])]
        #     self.all_dates[line[1]] = [x for x in tokens if x not in stops]
        #     for word in self.all_dates[line[1]]:
        #         self.alternative[word] = 0
        #         if word in self.null.keys():
        #             self.null[word] += 1
        #         else:
        #             self.null[word] = 1
        #         self.total += 1
        # for word in self.null.keys():
        #     self.null[word] /= self.total
        # print("time: " + str(time.time() - start))
        # file = open("null.txt", 'w', encoding="utf8")
        # for key in self.null.keys():
        #     file.write(key)
        #     file.write(' ')
        #     file.write(str(self.null[key]))
        #     file.write('\n')
        # file.close()
        # file = open("all_dates.txt", 'w', encoding="utf8")
        # for key in self.all_dates.keys():
        #     file.write(key)
        #     file.write(' ')
        #     file.write(str(self.all_dates[key]))
        #     file.write('\n')
        # file.close()
        # with open("null.json", 'w+') as f:
        #     json.dump(self.null, f)
        # with open("all_dates.json", 'w+') as f:
        #     json.dump(self.all_dates, f)
        #
        with open("null.json", 'r') as f:
            temp = json.loads(f.read())
        self.null = temp
        with open("all_dates.json", 'r') as f:
            temp = json.loads(f.read())
        self.all_dates = temp
        self.alternative = {word: 0 for word in self.null.keys()}
        print("time: " + str(time.time() - start))

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
        keys = self.null.keys()
        score = []
        for word in tokens:
            if word in keys:
                score.append(self.alternative[word] / self.null[word])
        return np.mean(np.array(score))


    def show_histogram(self, test, train):
        scores = []
        test_score = []
        train_score = []
        i = 0
        for date in self.all_dates.keys():
            if date in test:
                test_score.append(self.estimate_event(date))
            elif date in train:
                t = self.estimate_event(date)
                if t > 100:
                    continue
                train_score.append(t)
            else:
                if i > len(train_score):
                    continue
                else:
                    i += 1
                scores.append(self.estimate_event(date))
        print(len(test_score))
        print(len(train_score))
        print("kw p val: " + str(stat.kruskal(scores, test_score)[1]))
        thr = [1.4,1.9,2.3,2.5,2.7,3,3.5,4]
        tp, fp = [], []
        n, m = len(test_score), len(scores)
        for t in thr:
            tp.append(len([i for i in test_score if i>t])/n)
            fp.append(len([i for i in scores if i > t])/m)
        plt.plot([1]+ fp+[0], [1]+tp+[0])
        plt.plot([0,1],[0,1], color='k', linestyle='-', linewidth=2)
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.title("ROC curve")
        plt.savefig("ROC.png")
        plt.cla()
        plt.clf()
        plt.hist([scores, test_score, train_score], color=['b','r','y'],stacked=True, bins=70)
        plt.legend(['Non-Events', 'Test events', 'Train events'])
        plt.xlabel("Score")
        plt.ylabel("Number of events")
        plt.show()







es = EstimateLikelihood()
with open('data\\dates_and_percente_of_change_by_volume.txt', 'r') as f:
    reade = pd.read_table(f, header=None, index_col=None)
    reade.columns = ['dates','change']
    dates = np.array(reade.dates[abs(reade.change) > 65])
print(len(dates))
random.shuffle(dates)
print(len(dates))
train, test = dates[:80], dates[80:]
es.count_word_from_list_of_dates(np.array(train).ravel())
es.show_histogram(np.array(test).ravel(), np.array(train).ravel())
# es.estimate_event('2010-01-02')
# es.estimate_event('2010-01-03')
# es.estimate_event('2010-01-04')
# es.estimate_event('2010-01-05')
# es.estimate_event('2010-01-06')
# es.estimate_event('2010-01-07')
# es.estimate_event('2010-01-08')
# es.estimate_event('2010-01-09')
# es.estimate_event('2010-01-10')
# es.estimate_event('2011-08-05')
# es.estimate_event('2011-08-06')
# es.estimate_event('2011-08-07')
# es.estimate_event('2011-08-08')
# es.count_words_by_date("2011-01-04")




