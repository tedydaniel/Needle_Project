"""
This class should hold some function to analyze the stock using www.alphavantage.co data
"""

import urllib.request, json
import numpy as np
import matplotlib.pyplot as plt

tag = ['1. open', '2. high', '3. low', '4. close', '5. volume']
NumYears = 5
RangeMonth = 6

class StockData:


    def __init__(self, index):
        self.index = index
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.initializeData()

    def getDates(self):
        return self.dates

    def getOpens(self):
        return self.opens

    def getLows(self):
        return self.lows

    def getHighs(self):
        return self.highs

    def getCloses(self):
        return self.closes

    def getVolumes(self):
        return self.volumes


    def normalizedVolumes(self):
        """
        :return: Takes the ration of volume and the mean volume over about a year
        """
        indicies = []
        for i in range(self.dates[0].shape[0]):
            tmp_idx = [i]
            for j in range(1, len(self.dates)):
                tmp_idx += list(np.where(self.dates[j] == self.dates[0][i])[0])
            if len(tmp_idx) == len(self.dates):
                indicies.append(tmp_idx)
        indicies = np.array(indicies)
        volumes = np.zeros(indicies.shape[0]).astype(np.float64)
        for i in range(indicies.shape[1]):
            volumes += self.volumes[i][indicies[:, i]]
        volumes = volumes / np.mean(volumes)
        return volumes, indicies


    def initializeData(self, years = 6):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" +\
              self.index + "&outputsize=full&apikey=S86T4IDUATTIULH0"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())['Time Series (Daily)']

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



    def show_1_day_change(self, data, title = "No title"):
        np_data = np.array(data)
        to_sub = np.hstack((np.array([0]), np_data))
        to_plot = ((np_data - to_sub[:-1])/np_data) * 100
        # to_plot = to_plot / np.max(to_plot[1:])
        plt.plot(to_plot[1:])
        plt.title(title)
        plt.show()
        return to_plot


    def find_dates_with_change(self, data, treshold = 2):
        dates = []
        for i in range(len(data)):
            if data[i] > treshold or data[i] < -treshold:
                dates.append(self.dates[i])
        return dates





# #, 'SPXL', 'MSFT'
sd = StockData('NDAQ')
sd.show_1_day_change(sd.getHighs())
# print(sd.getOpens())

# plt.plot(range(len(sd.getOpens())),sd.getOpens())
# plt.title('Opens')
# plt.show()
# plt.plot(sd.getCloses())
# plt.title('Closes')
# plt.show()
# plt.plot(sd.getLows())
# plt.title('Lows')
# plt.show()
# plt.plot(sd.getHighs())
# plt.title('Highs')
# plt.show()
# plt.plot(sd.getVolumes())
# plt.title('Volumes')
# plt.show()

# volumes = sd.getVolumes()
# normVols, indicies = sd.normalizedVolumes()
# for v in range(len(volumes)):
#     plt.plot(volumes[v][indicies[:, v]] / np.mean(volumes[v][indicies[:, v]]))
# dates = np.array(sd.getDates())
# print(dates[0][np.where(normVols > 0)[0]])
# # plt.plot(normVols)
# plt.show()
# for vol in range(normVols.shape[0]):
#     print(dates[vol], normVols[vol])



