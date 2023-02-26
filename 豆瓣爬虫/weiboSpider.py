import json
import random
import time

import jieba
import numpy as np
import pandas as pd
import requests
from scrapy import Selector
import re
from wordcloud import WordCloud,ImageColorGenerator
import imageio

headers={
    'authority': 's.weibo.com',
    'method': 'GET',
    'path': '/weibo?q=%23%E7%94%84%E5%AC%9B%E4%BC%A0%E6%AF%8F%E5%B9%B4%E6%92%AD%E5%87%BA%E6%94%B6%E7%9B%8A%E4%BB%8D%E6%9C%89%E4%B8%8A%E5%8D%83%E4%B8%87%23',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': 'SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9Wh-Bp-wAbDDpLi8TnqTNdL7; SUB=_2AkMVqn8Kf8NxqwJRmP0XymvlboRywg7EieKj9o7RJRMxHRl-yj9jqksstRB6PipR5JZaAxW4HUpZ8PYT2RV72jOAyVqX; login_sid_t=d6e35b58d146d28270788c338d48243b; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=2324224111929.103.1660350527253; SINAGLOBAL=2324224111929.103.1660350527253; ULV=1660350527261:1:1:1:2324224111929.103.1660350527253:',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
proxies={
    'http':'http://127.0.0.1:19180',
    'https':'http://127.0.0.1:19180'
}
url='https://s.weibo.com/weibo?q=%23%E7%94%84%E5%AC%9B%E4%BC%A0%E6%AF%8F%E5%B9%B4%E6%92%AD%E5%87%BA%E6%94%B6%E7%9B%8A%E4%BB%8D%E6%9C%89%E4%B8%8A%E5%8D%83%E4%B8%87%23'
response=requests.get(url=url,headers=headers)
contents=''
sel=Selector(response)
selectors=sel.css('div.content')
for selector in selectors:
    content=''.join(re.findall(r'[\u4e00-\u9fa5]',''.join(selector.css('p[node-type=feed_list_content]::text').extract())))
    contents+=content
DATA=jieba.lcut(contents)
stopwords = [i.strip() for i in open('stopwords-master/hit_stopwords.txt', encoding='UTF-8').readlines()]
data=[]
for word in DATA:
    if word not in stopwords:
        data.append(word)
Data=''
i=0
while i <len(data):
    if data[i]=='甄':
        if data[i+1]=='嬛':
            if data[i+2]=='传':
                Data+=' '+'甄嬛传'
                i+=3
            else:
                Data+=' '+'甄嬛'
                i+=2
        else:
            Data+=data[i]
            i+=1
    else:
        Data+=' '+data[i]
        i+=1
font=r'SimHei.ttf'
wordcloud = WordCloud(background_color='black',max_words=100,font_path=font)
wordcloud.generate(Data)
wordcloud.to_file('微博热搜.jpg')

