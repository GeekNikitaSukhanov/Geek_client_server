import scrapy
from scrapy.http import HtmlResponse
from Lesson_6.jobparser_practice.items import JobparserPracticeItem

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        urls = response.xpath("//div[contains(@class,'_3zucV _2cmJQ _1SCYW')]//div[contains(@class, '_1h3Zg')]//a[contains(@class, 'icMQ_')]/@href").getall()
        next_page = response.xpath("//a[contains(@class, 'button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//div[contains(@class,'_3zucV _2cmJQ _1SCYW')]//div[contains(@class, '_1h3Zg')]//a[contains(@class, 'icMQ_')]/text()").get()
        #salary = response.xpath("//p[@class='vacancy-salary']").get()
        salary = response.css("span._1h3Zg _2Wp8I span::text").get()
        url = response.url
        item = JobparserPracticeItem(name=name, salary=salary, url=url)
        yield item







