# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    base_url = 'http://superjob.ru/vacancy/search/?keywords='
    vacancy_name = 'секретарь'
    start_urls = [f'{base_url + vacancy_name.replace(" ", "%20") + "&geo[t][0]=4"}']

    def parse(self, response):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_link = response.css('a._3dPok::attr(href)').extract()

        for link in vacancy_link:
            yield response.follow(link, self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_value('source', SjruSpider.name)
        loader.add_css('vacancy_name', 'div._3MVeX h1::text')
        loader.add_css('vacancy_company_name', 'a._2JivQ h2::text')
        loader.add_css('min_salary', 'span[class = "_3mfro _2Wp8I ZON4b PlM3e _2JVkc"] *::text')
        loader.add_value('max_salary', 'None')
        loader.add_value('currency', 'None')
        loader.add_value('url', response.url)
        yield loader.load_item()
