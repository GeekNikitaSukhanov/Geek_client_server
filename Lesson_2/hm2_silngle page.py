from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

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

pprint(roscontrol_list)