# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem


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
        source = HhruSpider.name
        vacancy_name = ' '.join(response.css('div.vacancy-title h1.header span.highlighted::text').extract() +
                                response.css('div.vacancy-title h1.header::text').extract())
        vacancy_company_name = response.css('a.vacancy-company-name span[itemprop="name"]::text').extract_first().strip()
        min_salary = response.css('div.vacancy-title meta[itemprop="minValue"]::attr(content)').extract_first()
        max_salary = response.css('div.vacancy-title meta[itemprop="value"]::attr(content), \
                                   div.vacancy-title meta[itemprop="maxValue"]::attr(content)').extract_first()
        currency = response.css('div.vacancy-title meta[itemprop="currency"] ::attr(content)').extract_first()
        url = response.url
#        print(source, vacancy_name, min_salary, max_salary, currency, url)
        yield JobparserItem(name=vacancy_name, company_name=vacancy_company_name, min_salary=min_salary,
                            max_salary=max_salary, currency=currency, url=url, resource=source)
