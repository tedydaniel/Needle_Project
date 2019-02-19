#  Name: 
#  Author: rotem.tal
#  Description:
#

import mechanicalsoup as ms
import datetime as dt
from stemming.porter2 import stem
import time


bro = ms.StatefulBrowser()
print([stem(word.lower()) for word in ['hospital', 'poland', 'workers']])
# s_date = int(time.mktime(dt.date(2017,1,1).timetuple()))
# e_date = int(time.mktime(dt.date(2017,1,2).timetuple()))
# term = "dummy"
# bro.open("https://redditsearch.io/?term="+term+"&dataviz=false&aggs=false&subreddits=&searchtype=posts&search=true"
#                                                "&start""=%s&end=%s&size=100"%(s_date, e_date))
# print(bro.get_current_page().find_all('div'))
# print(bro.get_current_page().html)