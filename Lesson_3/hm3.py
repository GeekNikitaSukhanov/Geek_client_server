'''
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать
 функцию, записывающую собранные вакансии в созданную БД.

2. Написать функцию, которая производит поиск и выводит на экран вакансии
с заработной платой больше введённой суммы (необходимо анализировать оба поля
зарплаты). Для тех, кто выполнил задание с Росконтролем -
напишите запрос для поиска продуктов с рейтингом не ниже введенного или
качеством не ниже введенного (то есть цифра вводится одна, а запрос проверяет
оба поля)

3. Написать функцию, которая будет добавлять в вашу базу данных только
новые вакансии с сайта.
'''

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo import MongoClient

url = 'https://roscontrol.com/product/moloko-ekomilk/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
           'Accept': '*/*'}

response_list = requests.get(url, headers=headers)
soup = bs(response_list.text, 'html.parser')
items = soup.find_all('div', attrs={'class': 'product__single'})
roscontrol_list = []
for item in items:
    item_dict = {}
    name = item.find('h1', attrs={'class': 'main-title testlab-caption-products util-inline-block'}).getText()
    score = item.find('div', attrs={'id': 'product__single-rev-total'}).getText().replace('\n', '').replace('Общая оценка', '')
    item_dict['name'] = name
    item_dict['score'] = score
    #item_dict['other_score'] = note_list
    roscontrol_list.append(item_dict)

other_scores = soup.find_all('div', attrs={'class': 'rate-item__value'})
score_list = []
for other_score in other_scores:
    scores_to_list = other_score.getText().replace('\n', '')
    score_list.append(scores_to_list)

roscontrol_list.append({'Безопасность': score_list[0], 'Натуральност': score_list[1],
                       'Пищевая ценность': score_list[2],'Качество': score_list[3]})

client = MongoClient('127.0.0.1', 27017)

db = client['products']

example = db.example

example.insert_one({'$set': roscontrol_list})

for item in example.find({}):
    pprint(item)