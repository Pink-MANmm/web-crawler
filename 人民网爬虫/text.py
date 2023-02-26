import time
import requests
from lxml import etree
import re
import pandas as pd
from loguru import logger
from datetime import datetime
import json
import urllib

url1='https://weiquan.people.com.cn/mini/com/complains/info'
headers1={
            #'Host':'weiquan.people.com.cn',
            #'Accept':'application/json, text/plain, */*',
            #'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
            #'Cookie':'ci_session=lupru4sjp71ql9q02pmltqom0loqt3e7',
            #'Referer':'https://weiquan.people.com.cn/',
            #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
info=requests.post(url=url1,headers=headers1)
print(json.loads(info.text))