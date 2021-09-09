import scrapy
from scrapy.http import HtmlResponse
from ..items import LeroyItem
from scrapy.loader import ItemLoader

#https://leroymerlin.ru/search/?q=%D0%BF%D0%BB%D0%B8%D1%82%D0%BA%D0%B0&family=40666520-5321-11ea-ad81-af309490eba8&suggest=true


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains =['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        add_links = response.xpath("//a[contains(@data-qa-pagination-item,'right')]")
        for link in add_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath('name', "//h1[contains(@slot, 'title')]/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[contains(@slot, 'primary-price')]/span[contains(@slot, 'price')]/text()")
        loader.add_xpath('params', "//uc-pdp-price-view[contains(@slot, 'primary-price')]/span[contains(@slot, 'unit')]/text()")
        loader.add_xpath('params', "//dl/text()")
        loader.add_xpath('url', "//uc-pdp-price-view//link/@href")
        loader.add_xpath('photos', "//uc-pdp-media-carousel//picture//img/@src")
        yield loader.load_item()
