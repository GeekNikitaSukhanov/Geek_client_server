# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstafollowingPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.insta

    def process_item1_insert(self, item, spider):
        collection = self.mongobase['followers']
        collection.insert_one(item)
        return item

    def process_item2_insert(self, item_1, spider):
        collection = self.mongobase['following']
        collection.insert_one(item_1)
        return item_1


