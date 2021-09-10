from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Instagram.instafollowing.instafollowing.spiders.insta import InstaSpider
from Instagram.instafollowing.instafollowing import settings

from sys import path
path.append('/Users/barin/Documents/GeekBrains/Data Sciense/Client_server/Instagram/instafollowing')

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaSpider)

    process.start()