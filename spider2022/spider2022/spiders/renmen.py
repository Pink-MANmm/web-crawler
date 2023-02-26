import scrapy
from scrapy import Selector,Request
from spider2022.items import requestItem


class RenmenSpider(scrapy.Spider):
    name = 'renmen'
    allowed_domains = ['weiquan.people.com.cn']
    start_urls = ['http://weiquan.people.com.cn/#/compsearch/-/-/-/-']

    def start_requests(self):
        yield Request(url='')
    def parse(self, response):
        sel=Selector(response)
        renmen_data=requestItem()
        yield renmen_data
