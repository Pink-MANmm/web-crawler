import requests
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import time
url='https://www.baidu.com/'
brower=Chrome()
brower.get(url)
html=brower.page_source
time.sleep(1)
content=brower.find_elements_by_xpath('//*[@id="hotsearch-content-wrapper"]/li/a/span[2]')
print(content)
for i in content:
    b=i.text
    print(b)