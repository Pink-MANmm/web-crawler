# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class requestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    requestTime=scrapy.Field()
    requestTitle=scrapy.Field()
    requestContent=scrapy.Field()
    answerTime=scrapy.Field()
    answerContent=scrapy.Field()
    pass
