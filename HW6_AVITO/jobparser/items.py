# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join
import scrapy


def array2str(values):
    values = values.strip()
    values = ''.join(values)
    return values


def currency_prepare(values):
    values = ''.join(values)
    values = values.replace('RUR', 'руб.')
    return values


def prepare_string(values):
    if values != ' ':
        values = values.replace(u'\xa0', u'')
        values = values.strip()
    else:
        values = None
    return values


class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    source = scrapy.Field(input_processor=MapCompose(array2str), output_processor=TakeFirst())
    vacancy_name = scrapy.Field(input_processor=MapCompose(array2str), output_processor=TakeFirst())
    vacancy_company_name = scrapy.Field(input_processor=MapCompose(array2str), output_processor=Join())
    min_salary = scrapy.Field(output_processor=TakeFirst())
    max_salary = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(input_processor=MapCompose(currency_prepare), output_processor=TakeFirst())
    url = scrapy.Field(input_processor=MapCompose(array2str), output_processor=TakeFirst())

