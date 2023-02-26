import time
import requests
from lxml import etree
import re
import pandas as pd
from loguru import logger
from datetime import datetime
import json

class sc():
    def __init__(self,page):
        '''初始化'''
        self.page=page
        self.url1='https://weiquan.people.com.cn/mini/com/complains/new'
        self.url2='https://weiquan.people.com.cn/mini/com/complains/info?id='
        self.id=[]
        self.headers1={
            'Host':'weiquan.people.com.cn',
            'Accept':'application/json, text/plain, */*',
            'Content-Type':'text/html; charset=UTF-8',
            'cookie':'ci_session=hhh522jn9v6cmnjtbncvmipn5pptn0k4',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        self.headers2={
            'cookie':'ci_session=4bc923u42j3r76tqaq0f53ufpbjq6ccp',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        self.formdata={
        'page': '1',
        'limit':'15',
        'from_id':'',
        }
        self.consultIndex=[]
        self.consultCategory = []
        self.consultTitle=[]
        self.consultContent = []
        self.consultName = []
        self.consultDate = []
        self.consultId = []
        self.consultState = []
        self.answerDate = []
        self.answerContent = []
        self.df = pd.DataFrame()
        self.currentYear=datetime.now().year
    def send1(self):
        '''发送请求'''
        self.id=[]
        info=requests.post(self.url1,headers=self.headers1,data=self.formdata)
        if info.status_code==200:
            Info = info.text
            Id = json.loads(Info)
            print(Id)
            for i in Id['data']['lists']:
                self.id.append(i['id'])
            print(self.id)
            return
    def send2(self,url):
        '''发送请求'''
        info = requests.get(url, headers=self.headers2)
        if info.status_code == 200:
            return info
    def spider(self):
        '''业务处理'''
        logger.info('开始启动爬虫')
        for pageNumber in range(1,self.page+1):
            logger.info('当前正在爬取第' + str(pageNumber) + '页')
            self.formdata['page']=str(pageNumber)
            print(self.url1+'page='+str(pageNumber)+'&limit=15&from_id=')
            self.send1()

        return

    '''每一小时采集一次数据'''
    def save(self):
        '''保存'''
        self.df['consultCategory'] = self.consultCategory
        self.df['consultTitle'] = self.consultTitle
        self.df['consultName']=self.consultName
        self.df['consultDate']=self.consultDate
        self.df['consultId']=self.consultId
        self.df['consultState']=self.consultState
        self.df['consultContent']=self.consultContent
        self.df['answerDate']=self.answerDate
        self.df['answerContent']=self.answerContent
        return

    def run(self):
        '''入口函数'''
        while True:
            self.spider()
        return
if __name__=='__main__':
    page=5
    sc(page).run()

