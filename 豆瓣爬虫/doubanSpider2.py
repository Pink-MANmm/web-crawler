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
    'Cookie': 'bid=xzugIknKe2Q; __yadk_uid=0DktyE0DuzWvIQLITJHebrbLcProlnqd; __gads=ID=3fbc33baa46d99a5-22dcf82c93d50027:T=1660349972:RT=1660349972:S=ALNI_MbzJ1L7ZY-oE2choYHlMDs4bJ3Zqg; dbcl2="260847986:nx32kZvyXLY"; ck=SRtf; __utmc=30149280; push_noty_num=0; push_doumail_num=0; __utmv=30149280.26084; __utmz=30149280.1660370491.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1660380530%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_ses.100001.8cb4=*; ap_v=0,6.0; __utma=30149280.463662546.1660349960.1660370491.1660380530.4; __utmt=1; __gpi=UID=0000088cbc7f8ac4:T=1660349972:RT=1660380531:S=ALNI_MaCh-bSVo_1UyBtaBYsapcr9i8wJA; _pk_id.100001.8cb4=5c1957e1bb2989d8.1660349971.3.1660380966.1660360344.; __utmb=30149280.32.8.1660380966547',
    'Host': 'www.douban.com',
    'Referer': 'https://www.douban.com/group/679420/discussion?start=50&type=new',
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
proxies={
    'http':'http://127.0.0.1:19180',
    'https':'http://127.0.0.1:19180'
}
contents=''
for page in range(20):
    print(page)
    if page==0:
        headers['Referer']='https://www.douban.com/group/679420/discussion?start=50&type=new'
    else:
        headers['Referer']='https://www.douban.com/group/679420/discussion?start='+str((page-1)*25)+'&type=new'
    response=requests.get(url='https://www.douban.com/group/679420/discussion?start='+str(page*25)+'&type=new',headers=headers)
    sel=Selector(response)
    selectors=sel.css('div.article > div:nth-child(2) > table.olt > tr')[1:]
    for selector in selectors:
        content=''.join(re.findall(r'[\u4e00-\u9fa5]',''.join(selector.css('td.title > a::text').extract())))
        print(content)
        contents+=' '+content
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
wordcloud.to_file('豆瓣小组讨论.jpg')