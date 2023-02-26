import time

import requests
from scrapy import Selector
import pandas as pd

df=pd.DataFrame()
userName=[]
Content=[]
Share=[]
Comment=[]
Like=[]
for page in range(1,30):
    print(page)
    url = f'https://s.weibo.com/weibo?q=唐山打人案宣判&page={page}'
    print(url)
    headers = {
        'authority': 's.weibo.com',
        'method': 'GET',
        'path': f'/weibo?q=%E5%94%90%E5%B1%B1%E6%89%93%E4%BA%BA%E6%A1%88%E5%AE%A3%E5%88%A4&page={page}',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '_s_tentry=passport.weibo.com; Apache=5969283656414.706.1665022930677; SINAGLOBAL=5969283656414.706.1665022930677; ULV=1665022930686:1:1:1:5969283656414.706.1665022930677:; PC_TOKEN=90e6456205; WBtopGlobal_register_version=2022100610; crossidccode=CODE-tc-1OGgx3-3Ifh9W-Rmaca7QYdOdx43pd81973; SSOLoginState=1665022967; SUB=_2A25OOkunDeThGeNG71UT8SvEyDSIHXVtxVXvrDV8PUJbkNAKLULNkW1NS0Q1QIB3HwHQmx1BuZfNOe7IqAcZBag8; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWQ_z6TnOh0pGceRqCnnI6V5NHD95Qf1hBNeo2f1heRWs4DqcjPi--ci-zEiKnRi--fiKLsiKy8SKBRe0zt',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    response=requests.get(url=url,headers=headers)
    sel=Selector(response)
    selectors=sel.css('div#pl_feedlist_index>div:nth-child(2)>div.card-wrap')
    for selector in selectors:
        if selector.css('div.card>div.card-feed>div.content>p[node-type="feed_list_content_full"]::attr(nick-name)').extract()!=[]:
            name=selector.css('div.card>div.card-feed>div.content>p[node-type="feed_list_content_full"]::attr(nick-name)').extract()[0]
            content=''.join(selector.css('div.card>div.card-feed>div.content>p[node-type="feed_list_content_full"]::text').extract())
        elif selector.css('div.card>div.card-feed>div.content>p[node-type="feed_list_content"]::attr(nick-name)').extract()!=[]:
            name = selector.css('div.card>div.card-feed>div.content>p[node-type="feed_list_content"]::attr(nick-name)').extract()[0]
            content = ''.join(selector.css('div.card>div.card-feed>div.content>p[node-type="feed_list_content"]::text').extract())
        if selector.css('div.card>div.card-act>ul>li:first-child>a::text').extract()[1]==' 转发':
            share=0
        else:
            share=selector.css('div.card>div.card-act>ul>li:first-child>a::text').extract()[1]
        if  selector.css('div.card>div.card-act>ul>li:nth-child(2)>a::text').extract()[0]==' 评论':
            comment=0
        else:
            comment=selector.css('div.card>div.card-act>ul>li:nth-child(2)>a::text').extract()[0]
        if selector.css('div.card>div.card-act>ul>li:nth-child(3)>a>button>span.woo-like-count::text').extract()[0]=='赞':
            like=0
        else:
            like=selector.css('div.card>div.card-act>ul>li:nth-child(3)>a>button>span.woo-like-count::text').extract()[0]
        userName.append(name)
        Content.append(content)
        Share.append(share)
        Comment.append(comment)
        Like.append(like)
    time.sleep(2)
print(userName,Content,Share,Comment,Like)
df['用户名']=userName
df['评论内容']=Content
df['分享数']=Share
df['评论数']=Comment
df['点赞数']=Like
df.to_excel('唐山打人案宣判.xlsx')