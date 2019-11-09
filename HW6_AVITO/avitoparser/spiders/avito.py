# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/avtomobili']

    def parse(self, response: HtmlResponse):
        # next_page = response.css('a.js-pagination-next::attr(href)').extract_first()
        # yield response.follow(next_page, callback=self.parse)

        ads_links = response.css('a.item-description-title-link::attr(href), \
                                  a.description-title-link::attr(href)').extract()
        for link in ads_links:
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_css('car_title', 'h1.title-info-title span.title-info-title-text::text')
        loader.add_value('car_url', response.url)
        loader.add_css('car_price', 'span.js-item-price::attr(content)')
        loader.add_css('currency', 'div.item-price-value-wrapper span.font_arial-rub::text')
        # loader.add_css('car_photos', 'div.gallery-img-frame > img')
        loader.add_xpath('car_photos', '//div[contains(@class, "gallery-img-wrapper")] \
                                        //div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('car_brand', 'div.item-view-block li:nth-of-type(1)')
        loader.add_css('car_model', 'div.item-view-block li:nth-of-type(2)')
        loader.add_css('car_generation', 'div.item-view-block li:nth-of-type(3)')
        loader.add_css('car_modification', 'div.item-view-block li:nth-of-type(4)')
        loader.add_css('manufacture_year', 'div.item-view-block li:nth-of-type(5)')
        loader.add_css('car_mileage', 'div.item-view-block li:nth-of-type(6)')
        loader.add_css('car_condition', 'div.item-view-block li:nth-of-type(7)')
        loader.add_css('car_owners', 'div.item-view-block li:nth-of-type(8)')
        loader.add_css('car_vin', 'div.item-view-block li:nth-of-type(9)')
        loader.add_css('body_style', 'div.item-view-block li:nth-of-type(10)')
        loader.add_css('door_quantity', 'div.item-view-block li:nth-of-type(11)')
        loader.add_css('engine_type', 'div.item-view-block li:nth-of-type(12)')
        loader.add_css('transmission_type', 'div.item-view-block li:nth-of-type(13)')
        loader.add_css('drive_type', 'div.item-view-block li:nth-of-type(14)')
        loader.add_css('steering_wheel', 'div.item-view-block li:nth-of-type(15)')
        loader.add_css('car_color', 'div.item-view-block li:nth-of-type(16)')
        loader.add_css('car_bundle', 'div.item-view-block li:nth-of-type(17)')
        loader.add_css('inspection_place', 'div.item-view-block li:nth-of-type(18)')
        loader.add_css('engine_volume', 'div.item-view-block li:nth-of-type(19)')
        yield loader.load_item()
