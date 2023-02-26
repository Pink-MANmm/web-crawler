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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'bid=xzugIknKe2Q; __gads=ID=3fbc33baa46d99a5-22dcf82c93d50027:T=1660349972:RT=1660349972:S=ALNI_MbzJ1L7ZY-oE2choYHlMDs4bJ3Zqg; __gpi=UID=0000088cbc7f8ac4:T=1660349972:RT=1660349972:S=ALNI_MaCh-bSVo_1UyBtaBYsapcr9i8wJA; dbcl2="260847986:nx32kZvyXLY"; ck=SRtf; __utmc=30149280; __utmc=223695111; push_noty_num=0; push_doumail_num=0; __utmv=30149280.26084; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1660370488%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.463662546.1660349960.1660360315.1660370491.3; __utmb=30149280.0.10.1660370491; __utmz=30149280.1660370491.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1794651015.1660349960.1660360315.1660370491.3; __utmb=223695111.0.10.1660370491; __utmz=223695111.1660370491.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/subject/4922787/reviews?start=40',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
headers2={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'bid=xzugIknKe2Q; __gads=ID=3fbc33baa46d99a5-22dcf82c93d50027:T=1660349972:RT=1660349972:S=ALNI_MbzJ1L7ZY-oE2choYHlMDs4bJ3Zqg; __gpi=UID=0000088cbc7f8ac4:T=1660349972:RT=1660349972:S=ALNI_MaCh-bSVo_1UyBtaBYsapcr9i8wJA; dbcl2="260847986:nx32kZvyXLY"; ck=SRtf; __utmc=30149280; __utmc=223695111; push_noty_num=0; push_doumail_num=0; __utmv=30149280.26084; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1660370488%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.463662546.1660349960.1660360315.1660370491.3; __utmb=30149280.0.10.1660370491; __utmz=30149280.1660370491.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1794651015.1660349960.1660360315.1660370491.3; __utmb=223695111.0.10.1660370491; __utmz=223695111.1660370491.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=d5d0961894c1d7cb.1660349960.3.1660371674.1660360315.',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/subject/4922787/reviews?start=0',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36X-Requested-With: XMLHttpRequest'
}
proxies={
    'http':'http://127.0.0.1:19180',
    'https':'http://127.0.0.1:19180'
}
contents=''
for page in range(25):
    print(page)
    headers['Referer']='https://movie.douban.com/subject/4922787/reviews?start='+str(page*20)
    headers2['Referer'] = 'https://movie.douban.com/subject/4922787/reviews?start=' + str(page * 20)
    response=requests.get(url='https://movie.douban.com/subject/4922787/reviews?start='+str(page*20),headers=headers)
    sel=Selector(response)
    ids=sel.css('div.review-list   > div[data-cid]::attr(data-cid)').extract()
    for id in ids:
        URL='https://movie.douban.com/j/review/'+str(id)+'/full'
        response2=requests.get(url=URL,headers=headers2).text
        content = ''.join(re.findall(r'[\u4e00-\u9fa5]', ''.join(json.loads(response2)['html'])))
        contents += content
    time.sleep(3)
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
wordcloud.to_file('豆瓣评论.jpg')
