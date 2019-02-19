"""
This class should hold some function to analyze the stock using www.alphavantage.co API.
Connection to internet required.
For now the main two indexes we work with are the NASDAQ and the DOW-JONES.
For each week (5 days) we perform t-test to filter by p-value.
"""

import urllib.request, json
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.stats import ttest_ind

tag = ['1. open', '2. high', '3. low', '4. close', '5. volume']
NumYears = 5
RangeMonth = 6

class StockData:


    def __init__(self, index='NDAQ'):
        self.index = index
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.initialize_data()



    def get_dates(self):
        return self.dates

    def get_opens(self):
        return self.opens

    def getLows(self):
        return self.lows

    def getHighs(self):
        return self.highs

    def getCloses(self):
        return self.closes

    def getVolumes(self):
        return self.volumes



    def sort_by_date(self, data, years = 15):
        for year in range(2018 - years, 2018):
            for month in range(1, 13):
                if month < 10:
                    month = '0' + str(month)
                for day in range(1, 32):
                    if day < 10:
                        day = '0' + str(day)
                    date = str(year) + '-' + str(month) + '-' + str(day)
                    if date in data.keys():
                        self.dates.append(date)
                        self.opens.append(float(data[date][tag[0]]))
                        self.highs.append(float(data[date][tag[1]]))
                        self.lows.append(float(data[date][tag[2]]))
                        self.closes.append(float(data[date][tag[3]]))
                        self.volumes.append(int(data[date][tag[4]]))



    def initialize_data(self):
        """
        :param years: num of years to look at
        :return: initializing the fields
        """
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" +\
              self.index + "&outputsize=full&apikey=S86T4IDUATTIULH0"
        response = urllib.request.urlopen(url)
        try:
            data = json.loads(response.read().decode())['Time Series (Daily)']
            self.sort_by_date(data=data)
        except KeyError:
            print("KeyError(Probably no network)")
            self.initialize_data()



    def show_1_day_change(self, data, title = "No title"):
        """
        :param data: the data to plot
        :param title: title
        :return: show a plot with the percent of the change from some day to the following day
        """
        np_data = np.array(data)
        to_sub = np.hstack((np.array([0]), np_data))
        to_plot = ((np_data - to_sub[:-1])/np_data) * 100
        plt.plot(to_plot[1:])
        plt.title(title)
        plt.show()
        return to_plot


    def find_dates_with_change(self, data, threshold = 2):
        """
        :param data: the data to look at
        :param treshold: change in percents, positive value
        :return:
        """
        dates = []
        for i in range(len(data)):
            if data[i] > threshold or data[i] < -threshold:
                dates.append((self.dates[i], data[i]))
        return dates


    def t_test(self, by='volumes', num_samples = 6):
        data = []
        if by == 'volumes':
            data = self.volumes
        elif by == 'closes':
            data = self.closes
        elif by == 'opens':
            data = self.opens
        elif by == 'highs':
            data = self.highs
        elif by == 'lows':
            data = self.lows
        sample1 = data[:num_samples]
        dates_to_pvals = {}
        for num in range(num_samples, len(data) - num_samples):
            sample2 = data[num:num + num_samples]
            if num + 2 < len(self.dates):
                dates_to_pvals[self.dates[num]] = ttest_ind(sample1, sample2)[1]
            sample1 = data[num - num_samples:num]
        return dates_to_pvals



def to_list_by_pval(data, pval=0.05):
    nas_sig = []
    for key in data.keys():
        if data[key] <= pval:
            nas_sig.append(key)
    return sorted(nas_sig)


def main():
    nasdaq = StockData(index='NDAQ')
    msft = StockData(index='MSFT')
    sp500 = StockData(index='^GSPC')
    dji = StockData(index='^DJI')
    rut = StockData(index='^RUT')
    print(to_list_by_pval(nasdaq.t_test(), pval=0.00001))
    print(to_list_by_pval(msft.t_test(), pval=0.00001))
    print(to_list_by_pval(sp500.t_test(), pval=0.00001))
    print(to_list_by_pval(dji.t_test(), pval=0.00001))
    print(to_list_by_pval(rut.t_test(), pval=0.00001))






if __name__ == '__main__':
    main()

