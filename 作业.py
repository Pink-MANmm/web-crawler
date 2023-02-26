import requests
from scrapy import Selector
import brotli

url='http://www.fanwen118.com/info_26/fw_3985026.html'
headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'SetCookieTF=1; testcookie=yes; Hm_lvt_ed68a17558fa716defd31aed4ebdc387=1663830391; FWFWUID=1663830448075e6y8o0f9qmpks3f; Hm_lpvt_ed68a17558fa716defd31aed4ebdc387=1663830453',
    'Host': 'www.fanwen118.com',
    'Referer': 'http://www.fanwen118.com/c/211928.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

response=requests.get(url=url,headers=headers)
#response.encoding="utf-8"
response.encoding = response.apparent_encoding

sel=Selector(response)
selectors=sel.css('p.t::text')
for selector in selectors:
    print(selector.extract())
