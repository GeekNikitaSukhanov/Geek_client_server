# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPracticePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies2808

    def process_item(self, item, spider):
        item['salary_min'], item['salary_max'], item['salary_cur'] = self.process_salary(item['salary'])
        del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):

        salary_elements_list = salary.split()
        salary_list = []
        for i in salary_elements_list:
            if i.isdigit():
                salary_list.append(i)
        if len(salary_list) > 2:
            salary_min = salary_list[0] + ' ' + salary_list[1]
            salary_max = salary_list[2] + ' ' + salary_list[3]
            currency_position = salary_elements_list.index(salary_list[2]) + 2
            salary_cur = salary_elements_list[currency_position].replace('<!--', ' ')
        else:
            salary_min = salary_list[0] + ' ' + salary_list[1]
            salary_max = ' '
            currency_position = salary_elements_list.index(salary_list[0]) + 2
            salary_cur = salary_elements_list[currency_position].replace('<!--', ' ')

        return salary_min, salary_max, salary_cur
