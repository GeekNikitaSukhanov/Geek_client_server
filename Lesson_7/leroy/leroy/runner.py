from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Lesson_7.leroy.leroy.spiders.leroy import LeroySpider
from Lesson_7.leroy.leroy import settings
from sys import path
path.append('/Users/barin/Documents/GeekBrains/Data Sciense/Client_server/Lesson_7/leroy')

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    #answer = input('Введите запрос ')
    process.crawl(LeroySpider, query='дрели')

    process.start()