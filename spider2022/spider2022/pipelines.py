# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql

class Spider2022Pipeline:

    def __init__(self):
        self.example=openpyxl.Workbook()
        self.data=self.example.active
        self.data.title='renminWeb'
        self.data.append(('title'))

    def close_spider(self,spider):
        self.example.save('人民网数据.xlsx')

    def process_item(self, item, spider):
        requestTitle=item.get('requestTitle','')
        self.example.append((requestTitle))
        return item
