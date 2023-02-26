import mysql
import requests
from selenium.webdriver import Chrome
import time
from bs4 import BeautifulSoup
from tool import get_conn
from tool import close
import json


def get_hotdata():
    url = 'https://top.baidu.com/board?tab=homepage'
    brower = Chrome()
    brower.get(url)
    html = brower.page_source
    time.sleep(1)
    btn=brower.find_element_by_xpath('//*[@id="sanRoot"]/header/div[2]/div[2]/a[2]/span')
    btn.click()
    time.sleep(1)
    content=brower.find_elements_by_xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/div[2]/a/div[1]')
    content2=brower.find_elements_by_xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/div[1]/div[2]')
    hotdata=[]
    num=0
    for item in content:
        i=item.text
        b=content2[num]
        a=b.text
        x=i+a
        hotdata.append(x)
        num+=1
    print(hotdata)
    return hotdata

def insert_hotdata():
    conn,cursor=get_conn()
    sql='insert into hotsearch(dt,content) values(%s,%s)'
    datas=get_hotdata()
    dt=time.strftime('%Y-%m-%d %X')
    for item in datas:
        cursor.execute(sql,(dt,item))
        conn.commit()
    print('数据插入成功')
    close(conn,cursor)

def get_history():
    history={}
    url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0'
        ,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41'
    }
    resp=requests.get(url=url,headers=headers)
    jsondata=resp.text
    data=json.loads(jsondata)
    chinadata=json.loads(data['data'])
    for day in chinadata['chinaDayList']:
        dt='2020.'+day['date']
        tup=time.strptime(dt,'%Y.%m.%d')
        dt=time.strftime('%Y-%m-%d',tup)
        confirm=day['confirm']
        suspect=day['suspect']
        heal=day['heal']
        dead=day['dead']
        history[dt]={'confirm':confirm,'suspect':suspect,'heal':heal,'dead':dead}
    for dayadd in chinadata['chinaDayAddList']:
        dt = '2020.' + dayadd['date']
        tup = time.strptime(dt, '%Y.%m.%d')
        dt = time.strftime('%Y-%m-%d', tup)
        confirm_add=dayadd['confirm']
        suspect_add=dayadd['suspect']
        heal_add=dayadd['heal']
        dead_add=dayadd['dead']
        history[dt].update({'confirm_add':confirm_add,'suspect_add':suspect_add,'heal_add':heal_add,'dead_add':dead_add})
    print(history)
    return history

def insert_history():
    conn,cursor=get_conn()
    history=get_history()
    sql='insert into history(ds,confirm,confirm_add,suspect,suspect_add,heal,heal_add,dead,dead_add) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for k,v in history.items():
        cursor.execute(sql,[k,v.get('confirm'),v.get('confirm_add'),v.get('suspect'),v.get('suspect_add'),v.get('heal'),v.get('heal_add'),v.get('dead'),v.get('dead_add')])
        conn.commit()
    close(conn,cursor)
    print('插入成功')

def get_details():
    url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0'
        ,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41'
    }
    resp=requests.get(url,headers)
    time.sleep(1)
    jsondata=resp.text
    data=json.loads(jsondata)
    jsondetails=data['data']
    details=json.loads(jsondetails)
    updatetime=details['lastUpdateTime']
    content=details['areaTree']
    country=content[0]
    provinces=country['children']
    detailsdata=[]
    for province in provinces:
        cities=province['children']
        for city in cities:
            confirm=city['total']['confirm']
            confirm_add=city['today']['confirm']
            heal=city['total']['heal']
            dead=city['total']['dead']
            a=[]
            a.append(updatetime)
            a.append(province['name'])
            a.append(city['name'])
            a.append(confirm)
            a.append(confirm_add)
            a.append(heal)
            a.append(dead)
            detailsdata.append(a)
    #print(detailsdata)
    return detailsdata
def insert_details():
    conn,cursor=get_conn()
    detailsdata=get_details()
    sql='insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)'
    sql_query='select %s=(select update_time from details order by id desc limit 1)'
    cursor.execute(sql_query,detailsdata[0][0])
    if not cursor.fetchone()[0]:
        print('开始更新数据')
        for i in detailsdata:
            cursor.execute(sql,(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
            conn.commit()
        close(conn,cursor)
        print('数据更新成功')
    else:
        print('已经是最新数据，无需更新！')
get_hotdata()




