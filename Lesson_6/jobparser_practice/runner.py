from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from jobparser import settings
from Lesson_6.jobparser_practice.spiders.hhru import HhruSpider
from Lesson_6.jobparser_practice.spiders.superjob import SuperjobSpider
if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SuperjobSpider)

    process.start()











