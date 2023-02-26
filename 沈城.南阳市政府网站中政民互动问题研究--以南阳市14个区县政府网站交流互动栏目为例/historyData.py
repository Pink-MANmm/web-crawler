import time
import requests
from lxml import etree
import re
import pandas as pd
from loguru import logger
from datetime import datetime

class sc():
    def __init__(self,page):
        '''初始化'''
        self.page=page
        self.url='http://m.01ny.cn/forum/search/all.shtml?pageNo='
        self.headers={
            'cookie':'__yjs_duid=1_f810100e32c9945459334cbf804fabcc1654169408682; Hm_lvt_43696acba0a5f0a8b12c20d353498f02=1654169410,1654229506; Hm_lpvt_43696acba0a5f0a8b12c20d353498f02=1654230297',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        self.consultCategory = []
        self.consultTitle = []
        self.consultContent = []
        self.consultName = []
        self.consultDate = []
        self.consultId = []
        self.consultDepartment = []
        self.consultState = []
        self.answerDepartment = []
        self.answerDate = []
        self.answerContent = []
        self.df = pd.DataFrame()
        self.currentYear=datetime.now().year
    def send(self,url):
        '''发送请求'''
        info=requests.get(url,headers=self.headers)
        if info.status_code==200:
            return info
    def spider(self):
        '''业务处理'''
        logger.info('开始启动爬虫')
        for pageNumber in range(1,self.page+1):
            logger.info('当前正在爬取第' + str(pageNumber) + '页')
            info=self.send(self.url+str(pageNumber))
            html=etree.HTML(info.text)
            item=html.xpath('//div[@class="bm-left"]/div[@class="bm-index-list"]')
            for i in item:
                href=i.xpath('.//span[@class="hei18cu"]/a/@href')
                url1='http://m.01ny.cn'+href[0]
                detailInfo=self.send(url1)
                detailHtml=etree.HTML(detailInfo.text)
                askCategory=''.join(re.findall(r'[\u4e00-\u9fa5]',detailHtml.xpath('//h4/span/text()')[0]))
                askTitle=detailHtml.xpath('//h4/strong/text()')[0]
                askContent=''.join(re.findall(r'[\u4e00-\u9fa5]',detailHtml.xpath('//div[@class="ask-summary mt10"]/text()')[0]))
                askName=''.join(re.findall(r'[\u4e00-\u9fa5]',detailHtml.xpath('//div[@class="ask-info"]/span[@class="ask-user"]/text()')[0]))
                askDate=''.join(detailHtml.xpath('//div[@class="ask-info"]/span[@class="ask-date"]/text()')[0])
                askId=''.join(detailHtml.xpath('//div[@class="ask-info"]/span[@class="ask-date"]/em/text()')[0])
                askDepartment=''.join(re.findall(r'[\u4e00-\u9fa5]',detailHtml.xpath('//span[@class="ask-depart fr"]/text()')[0]))
                askState=''.join(re.findall(r'[\u4e00-\u9fa5]',detailHtml.xpath('//span[@class="ask-depart fr"]/em/text()')[0]))
                reply=detailHtml.xpath('//div[@class="bmhf"]/text()')
                data1= lambda reply:detailHtml.xpath('//span[@class="bmmc"]/strong/text()')[0] if reply!=[] else ''
                data2= lambda reply:detailHtml.xpath('//span[@class="hfsj"]/text()')[-1] if reply!=[] else ''
                data3 = lambda reply: ''.join(re.findall(r'[\u4e00-\u9fa5]',detailHtml.xpath('//div[@class="huifuneirong"]')[-1].xpath('string(.)').replace(' ',''))) if reply != [] else ''
                replyDepartment=data1(reply)
                replyDate=data2(reply)
                replyContent=data3(reply)
                '''去重'''
                if askId not in self.consultId and (askDate[0:4]==str(self.currentYear) or askDate[0:4]==str(self.currentYear-1)):
                    self.consultCategory.append(str(askCategory))
                    self.consultName.append(askName)
                    self.consultDate.append(askDate)
                    self.consultId.append(askId)
                    self.consultTitle.append(askTitle)
                    self.consultDepartment.append(askDepartment)
                    self.consultContent.append(askContent)
                    self.consultState.append(askState)
                    self.answerDate.append(replyDate)
                    self.answerContent.append(replyContent)
                    self.answerDepartment.append(replyDepartment)
                else:
                    logger.info('数据更新完毕')
                    logger.info('下一次数据采集将在一小时后')
                    self.save()
                    self.df.to_excel('hd.xlsx')
                    '''实现增量，源源不断获取最新版本的数据文件'''
                    self.df.drop(self.df.index, inplace=True)
                    time.sleep(60*60)
                    '''每一小时采集一次数据'''
                    self.spider()
        return
    def save(self):
        '''保存'''
        self.df['consultCategory'] = self.consultCategory
        self.df['consultTitle'] = self.consultTitle
        self.df['consultName']=self.consultName
        self.df['consultDate']=self.consultDate
        self.df['consultId']=self.consultId
        self.df['consultDepartment']=self.consultDepartment
        self.df['consultState']=self.consultState
        self.df['consultContent']=self.consultContent
        self.df['answerDepartment']=self.answerDepartment
        self.df['answerDate']=self.answerDate
        self.df['answerContent']=self.answerContent
        return

    def run(self):
        '''入口函数'''
        while True:
            self.spider()
        return
if __name__=='__main__':
    page=1000
    sc(page).run()

