# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def get_price(value):
    try:
        value = int(value.replace('\xa0', ' '))
    except Exception:
        pass
    return value


class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst)
    price = scrapy.Field(input_processor=MapCompose(get_price), output_processor=TakeFirst())
    unit = scrapy.Field(input_processor=MapCompose(get_price), output_processor=TakeFirst())
    params = scrapy.Field()
    url = scrapy.Field()
    photos = scrapy.Field()


