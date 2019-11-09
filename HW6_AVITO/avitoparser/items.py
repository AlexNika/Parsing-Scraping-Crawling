# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose, TakeFirst
import scrapy


def cleaner_photo(values):
    if values[:2] == '//':
        return f'https:{values}'
    return values


def price2int(price):
    try:
        price_in_digit = int(price)
        return price_in_digit
    except ValueError as e:
        print(e)


def prepare_string(values):
    if values != ' ':
        values = values.replace(u'\xa0', u'')
    else:
        values = None
    return values


def prepare_car_description(values):
    # <li class="item-params-list-item"> <span class="item-params-label"XXXXXX </span>XXXXXX </li>
    if values != ' ':
        values = values.replace('<li class="item-params-list-item"> <span class="item-params-label">', '')
        values = values.replace('</span>', '')
        values = values.replace('</li>', '')
        values = values.replace(': ', ' - ')
        values = values.rstrip()
    return values


class AvitoparserItem(scrapy.Item):
    _id = scrapy.Field()
    car_title = scrapy.Field(output_processor=TakeFirst())
    car_url = scrapy.Field(output_processor=TakeFirst())
    car_price = scrapy.Field(input_processor=MapCompose(price2int), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    car_photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    car_brand = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    car_model = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    car_generation = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    car_modification = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    manufacture_year = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    car_mileage = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    car_condition = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    car_owners = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    car_vin = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    body_style = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    door_quantity = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    engine_type = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    transmission_type = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    drive_type = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    steering_wheel = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    car_color = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    car_bundle = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    inspection_place = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())
    engine_volume = scrapy.Field(input_processor=MapCompose(prepare_car_description), output_processor=TakeFirst())