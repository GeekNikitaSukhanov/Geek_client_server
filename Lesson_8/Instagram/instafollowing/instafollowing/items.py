# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstafollowingItem(scrapy.Item):
    # define the fields for your item here like:
    account_id = scrapy.Field()
    account_name = scrapy.Field()
    follower_id = scrapy.Field()
    follower_name = scrapy.Field()
    follower_photo = scrapy.Field()


class InstafollowingItem_2(scrapy.Item):
    # define the fields for your item here like:
    account_id = scrapy.Field()
    account_name = scrapy.Field()
    following_id = scrapy.Field()
    following_name = scrapy.Field()
    following_photo = scrapy.Field()