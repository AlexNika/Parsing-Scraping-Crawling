# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.db_GB_PSC_HW5

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            if item['min_salary'] is not None:
                try:
                    item['min_salary'] = int(item['min_salary'])
                except ValueError:
                    pass
            if item['max_salary'] is not None:
                try:
                    item['max_salary'] = int(item['max_salary'])
                except ValueError:
                    pass
        if spider.name == 'sjru':
            salary = item['min_salary']
            item['min_salary'], item['max_salary'], item['currency'] = self.sjru_salary_parse(salary)
#        print(item, spider)
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    @staticmethod
    def sjru_salary_parse(min_salary):
        s_min = None
        s_max = None
        currency = ''
        if len(min_salary) == 3:
            s_min = min_salary[0].replace('\xa0', '')
            currency = min_salary[-1]
            try:
                s_min = int(s_min)
            except ValueError:
                pass
        elif len(min_salary) == 5:
            if min_salary[0] == 'от':
                s_min = min_salary[2].replace('\xa0', '')
                currency = min_salary[-1]
                try:
                    s_min = int(s_min)
                except ValueError:
                    pass
            if min_salary[0] == 'до':
                s_max = min_salary[2].replace('\xa0', '')
                currency = min_salary[-1]
                try:
                    s_max = int(s_max)
                except ValueError:
                    pass
        elif len(min_salary) == 7:
            s_min = min_salary[0].replace('\xa0', '')
            s_max = min_salary[4].replace('\xa0', '')
            currency = min_salary[-1]
            try:
                s_min = int(s_min)
            except ValueError:
                pass
            try:
                s_max = int(s_max)
            except ValueError:
                pass
        return s_min, s_max, currency
