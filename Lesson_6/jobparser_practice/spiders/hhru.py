import scrapy
from scrapy.http import HtmlResponse
from Lesson_6.jobparser_practice.items import JobparserPracticeItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=python&area=1',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=python&area=2']

    def parse(self, response: HtmlResponse):
        urls = response.xpath("//a[contains(@data-qa, 'vacancy-serp__vacancy-title')]/@href").getall()
        next_page = response.xpath("//a[contains(@data-qa, 'pager-next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        #salary = response.xpath("//p[@class='vacancy-salary']").get()
        salary = response.css("p.vacancy-salary span::text").get()
        url = response.url
        item = JobparserPracticeItem(name=name, salary=salary, url=url)
        yield item






