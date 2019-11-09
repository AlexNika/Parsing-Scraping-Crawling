# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem


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
        source = SjruSpider.name
        vacancy_name = response.css('div._3MVeX h1::text').extract_first()
        vacancy_company_name = response.css('a._2JivQ h2::text').extract_first()
        min_salary = response.css('span[class = "_3mfro _2Wp8I ZON4b PlM3e _2JVkc"] *::text').extract()
        max_salary = None
        currency = None
        url = response.url
#        print(source, vacancy_name, min_salary, max_salary, currency, url)
        yield JobparserItem(name=vacancy_name, company_name=vacancy_company_name, min_salary=min_salary,
                            max_salary=max_salary, currency=currency, url=url, resource=source)
