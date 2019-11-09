# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    base_url = 'https://hh.ru/search/vacancy?area=1&text='
    vacancy_name = 'секретарь'
    start_urls = [f'{base_url + vacancy_name.replace(" ", "+")}']

    def parse(self, response):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_link = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)'
        ).extract()

        for link in vacancy_link:
            yield response.follow(link, self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_value('source', HhruSpider.name)
        loader.add_value('source', HhruSpider.name)

        loader.add_value('source', HhruSpider.name)
        loader.add_xpath('vacancy_name', '//div[@class="vacancy-title"]//h1[@class="header"]/ \
                                         span[@class="highlighted"]/text() | //div[@class="vacancy-title"]// \
                                         h1[@class="header"]/span/text()')
        loader.add_xpath('vacancy_company_name', '//a[@class="vacancy-company-name"]/span[@itemprop="name"]/text() | \
                                                  //a[@class="vacancy-company-name"]/span[@itemprop="name"]/span/ \
                                                  text()')
        loader.add_css('min_salary', 'div.vacancy-title meta[itemprop="minValue"]::attr(content)')
        loader.add_css('max_salary', 'div.vacancy-title meta[itemprop="value"]::attr(content), \
                                      div.vacancy-title meta[itemprop="maxValue"]::attr(content)')
        loader.add_css('currency', 'div.vacancy-title meta[itemprop="currency"] ::attr(content)')
        loader.add_value('url', response.url)
        # print(loader)
        yield loader.load_item()
