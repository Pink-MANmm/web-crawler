import json
import random
import time

import pandas as pd
import requests

headers={
    'authority': 'club.jd.com',
    'method': 'GET',
    'path': '/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100021250873&score=3&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': 'unpl=JF8EAJhnNSttDUldAB9VS0AYSVtVW1hbGR4FbTAABAhfSwBSHgQeEhh7XlVdXhRKHh9uYBRVVFNOVA4ZASsSEXteU11bD00VB2xXXAQDGhUQR09SWEBJJVlQXl4ITxcFZ2A1ZF5Ye1QEKwIYFxRPXF1cVQB7JwRfVzVWW1lNVg0rAysTIAkJCFZfCU0RASJnBlFZXEpdBxMKKxMgSA; __jdv=76161171|haosou-search|t_262767352_haosousearch|cpc|5512151796_0_d3845fac937044bc873f4ad61ef47419|1659746493146; __jdu=1245508399; areaId=22; PCSYCityID=CN_510000_510600_0; shshshfpa=8fed88b2-5b57-bb15-ebea-0d25640136af-1659746496; shshshfpb=z9tlpMfgGxwJgmFqJBhm2-g; __jdc=122270672; shshshfp=02a55c41c6c8a27285ba0324d9537203; ip_cityCode=1962; ipLoc-djd=22-1962-39010-39111; jwotest_product=99; __jda=122270672.1245508399.1659746491.1659768127.1659782293.4; jsavif=1; token=50ad86288a7e82783b7f31cdf87de239,2,922101; __tk=kUj5kpbpIsnEjijEkUhTkvfhkvIyjpfokiJojpI1jvn5IDa1JUezkG,2,922101; shshshsID=cadd85abd0d237d9d6604c08f297faca_5_1659782539437; __jdb=122270672.5.1245508399|4.1659782293; 3AB9D23F7A4B3C9B=EVVJPSR7PLB6OK4MRC7PQCSXV2ZHUTYN4KSUENQB5D2C5NPQDQEBNG6C5XOCLD26OUV2YRHSXAU3DLE3PX5QWXTMMM; JSESSIONID=D5933D530C6D9D5623E1C59053C3D981.s1',
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
def Spider(productID,score,productName):
    df=pd.DataFrame()
    content=[]
    voteCount=[]
    VIP=[]
    Date=[]
    for page in range(1000):
        print(page)
        if page==0:
            url='https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId='+str(productID)+'&score='+str(score)+'&sortType=5&page='+str(page)+'&pageSize=10&isShadowSku=0&fold=1'
            headers['path']='/comment/productPageComments.action?callback=fetchJSON_comment98&productId='+str(productID)+'&score='+str(score)+'&sortType=5&page='+str(page)+'&pageSize=10&isShadowSku=0&fold=1'
            response = json.loads(requests.get(url=url, headers=headers).text.replace('fetchJSON_comment98(', '')[:-2])
        else:
            url='https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId='+str(productID)+'&score='+str(score)+'&sortType=5&page='+str(page)+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
            headers['path']='/comment/productPageComments.action?callback=fetchJSON_comment98&productId='+str(productID)+'&score='+str(score)+'&sortType=5&page='+str(page)+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
            response = json.loads(requests.get(url=url, headers=headers).text.replace('fetchJSON_comment98(', '')[:-2])
        comments=response['comments']
        for comment in comments:
            cont=comment['content']
            vote=comment['usefulVoteCount']
            date=comment['creationTime']
            if comment['plusAvailable']==201:
                vip='PLUS会员'
            else:
                vip='普通用户'
            print(cont +'/'+ str(vote) +'/'+ vip+'/'+str(comment['plusAvailable'])+'/'+str(comment['creationTime']))
            content.append(cont)
            voteCount.append(vote)
            VIP.append(vip)
            Date.append(date)
        time.sleep(random.randint(1,3))
    df['内容']=content
    df['点赞']=voteCount
    df['会员状态']=VIP
    df['日期']=Date
    df.to_excel(str(productName)+'.xlsx')
Spider(259348,1,'迪奥Dior真我香氛/女士香水100ml--差评')
Spider(259348,2,'迪奥Dior真我香氛/女士香水100ml--中评')
Spider(259348,3,'迪奥Dior真我香氛/女士香水100ml--好评')