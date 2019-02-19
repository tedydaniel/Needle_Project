#  Name: 
#  Author: rotem.tal
#  Description:
#
import nltk
import pandas as pd
import mechanicalsoup as ms
from nytimesarticle import articleAPI
from newsapi import NewsApiClient
from stemming.porter2 import stem as st
from matplotlib.pyplot import *
from collections import Counter
from itertools import groupby
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
import numpy as np

# start = '2015-09-1'
reddit = pd.read_csv("reddit.csv", header=0)
reddit = reddit.drop(["subreddit", "author", "over_18", "time_created"], 1)
vec = TfidfVectorizer(analyzer='word', stop_words='english',token_pattern='\w\w+|u s',ngram_range=(1,3),max_features=20)
dates = pd.read_table("dates.txt", header=None)
dates.columns = ['dates', 'change']
dates = dates.drop([i for i in dates.index if int(dates.dates[i].split("-")[0]) >= 2017 or
                    int(dates.dates[i].split("-")[0]) <= 2008])
important_dates = dates.dates[abs(dates.change) > 2.5]
important_dates = important_dates.drop([i for i in important_dates.index if i+1 in important_dates.index])

train = important_dates.sample(frac=0.7,random_state=200)
test = important_dates.drop(train.index)
tfid_graph = nx.MultiGraph()
tok_graph = nx.MultiGraph()
unique_dates = pd.Series(reddit.date_created.unique())
# print(reddit.title[reddit.date_created == '2008-02-01'])
# print(reddit.date_created)
# mat = reddit.title[(reddit.date_created == start+'3') | (reddit.date_created == start+'4')
#                    | (reddit.date_created == start+'5') | (reddit.date_created == start+'6')
#                    | (reddit.date_created == start+'7')]
print(len(train))
for date in train:
    try:
        ind = unique_dates[unique_dates==date].index[0]
    except Exception as e:
        print(date)
        continue
    print(ind)
    # start = date[:-1]
    # d_date = int(date[-1])
    # if d_date <= 4:
    #     spl = start.split("-")
    #     week = int(spl[2])
    #     if week:
    #         rep = "-%s-%s"%(spl[1], week-1)
    #     else:
    #         rep = "-0%s-2"%str(int(spl[1])-1) if int(spl[1])<=10 else "-1%s-2"+str(int(spl[1]-11))
    #     start = spl[0]+rep
    #     s_date = 5 + d_date
    # else:
    #     s_date = d_date - 5
    for i in range(6):
        # if i + s_date == 10:
        #     s_date = -i
        #     start = start[:-1]+ str(int(start[-1])+1)
        mat = reddit.title[reddit.date_created == unique_dates[ind-i]]
        X = vec.fit_transform(mat)
        tokens = list(map(nltk.RegexpTokenizer(r'\w\w+|U S').tokenize, mat))
        tokens = list(map(lambda x:list(filter(lambda word: word.lower() not in nltk.corpus.stopwords.words('english'), x)),
                          tokens))
        tokens = [st(tok.lower()) for subl in tokens for tok in subl if tok.lower()]
        # try:
        #     tokens = list(map(stem, tokens))
        # except Exception as e:
        #     continue
        # print(Counter(tokens))
        # print(vec.get_feature_names())
        # print(Counter(tokens).keys())
        tfid_graph.add_node(date, data=vec.get_feature_names())
        tok_graph.add_node(date, data=list(zip(*Counter(tokens).most_common(20)))[0][:20])
data_tfid = nx.get_node_attributes(tfid_graph, 'data')
data_tok = nx.get_node_attributes(tok_graph, 'data')
intersects_tfid = {date1: {date2: set(data_tfid[date1]).intersection(set(data_tfid[date2])) for date2 in train
                           if date2 != date1} for date1 in train}
intersects_tok = {date1: {date2: set(data_tok[date1]).intersection(set(data_tok[date2])) for date2 in train
                           if date2 != date1} for date1 in train}

tfid_graph.add_edges_from([(date1, date2, {'common': intersects_tfid[date1][date2],
                                           'weight':len(intersects_tfid[date1][date1])}) for date1 in train for date2 in
                           train if date1 != date2 and len(intersects_tfid[date1][date2])])
tok_graph.add_edges_from([(date1, date2, {'common': intersects_tok[date1][date2],
                                          'weight': len(intersects_tok[date1][date1])}) for date1 in train for date2 in
                           train if date1 != date2 and len(intersects_tok[date1][date2])])
with open("tfidWeight", 'wb') as tf, open("tokenWeightg", 'wb') as tk:
    nx.write_edgelist(tfid_graph, tf)
    nx.write_edgelist(tok_graph, tk)
nx.draw(tfid_graph, with_labels=True)
# savefig("tdif_graph.png")
labels = nx.get_edge_attributes(tfid_graph,'weight')
nx.draw_networkx_edge_labels(tfid_graph,edge_labels=labels)
show()
nx.draw(tok_graph, with_labels=True)
# savefig("tok_graph.png")
show()
# tokens = {k:tuple(x[1] for x in v) for k, v in groupby(sorted(tokens), key=lambda x: x[0])}
# print(tokens)
# for i in range(7,3,-1):
#     date = start + str(i)


# bro = ms.StatefulBrowser()
# lnk_b = ms.StatefulBrowser()
# goal_reached = False
# cur_page = 1
# while not goal_reached:
#     bro.open("https://www.nytimes.com/by/andrew-ross-sorkin")
#     pre_l = bro.get_current_page().find_all('div', attrs={'class': "story-body"})
#     for link in pre_l:
#         lnk_b.open(link.a.get('href'))
#         art = lnk_b.get_current_page().article.text
#         tokens = nltk.RegexpTokenizer(r'\w+').tokenize(art)
#         sw_tok = list(filter(lambda word: word.lower() not in nltk.corpus.stopwords.words('english'), tokens))
#         count = Counter(sw_tok)
#         break
#     break
# d = pd.read_csv('RedditNews.csv', header=0)
# heads = d['2013-03-26' ==d['Date']]
# for i in range(7,10):
#     heads = heads.append(d[d['Date'] == '2013-03-2'+str(i)])
# heads = heads.append(d[d['Date'] == '2013-04-01'])
# print(heads)
# tok = list(map(nltk.pos_tag, map(nltk.word_tokenize, heads['News'])))
# print(tok)
# print(head)
# api = articleAPI("5a7ce92d987b45d39cb1310c69f02f26")
# # articles = api.search(q='economy',begin_date=20130326 ,end_date=20130327)
# financial_times_key = "59cbaf20e3e06d3565778e7b6ddaf9ae782c4cdabccf2a9f10893475"
# newsapi_key = "f5d7c49099ae4bb68c32a2e164edd06b"
# newsapi_client = NewsApiClient(api_key=newsapi_key)
# articles = newsapi_client.get_everything(sources='the-wall-street-journal',
#                                       language='en',
#                                       sort_by='relevancy',
#                                          from_param='2017-12-01', to='2017-12-12')
# print(articles)
# for i in range (1,9):
#     print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
#     articles = api.search(begin_date=20130326 ,end_date=20130326, page=i)
#     try:
#         for i in articles['response']['docs']:
#     # print(i['headline'])
#             print(i['snippet'])
#     # print(i['keywords'])
#             print(i['pub_date'])
#     except:
#         print(i)
#         print(articles)
    # print(i['news_desk'])
    # print(i['score'])
    # print(i.keys())
# df = pd.read_table("2018.csv", sep='\t')
# print(df)
