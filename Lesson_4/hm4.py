'''
Написать приложение, которое собирает основные новости с сайта на выбор lenta.ru,
news.mail.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
Сложить собранные данные в БД
'''


from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
           'Accept': '*/*'}
url = 'https://lenta.ru/'
response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)
main_news = dom.xpath("//div//section[contains(@class, 'row b-top7-for-main js-top-seven')]")
news_list = []
for item in main_news:
    news_item = item.xpath(".//div[contains(@class, 'item')]")
    for i in news_item:
        news_dict = {}
        link = i.xpath("./a/@href")
        date = i.xpath(".//a/time/@title")
        name = i.xpath(".//a//text()")
        name.remove(name[0])
        if len(name) > 1:
            name.remove(name[1])
            name_upd = name[0].replace('\xa0', ' ')
        else:
            name_upd = name[0].replace('\xa0', ' ')

        news_dict['link'] = link
        news_dict['date'] = date
        news_dict['name'] = name_upd

        news_list.append(news_dict)

client = MongoClient('127.0.0.1', 27017)

db = client['news']

main_news = db.main_news
for item in news_list:
    main_news.insert_one(item)

for item in main_news.find({}):
    pprint(item)

