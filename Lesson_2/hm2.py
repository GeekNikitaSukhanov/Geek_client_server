'''
Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы получаем должность) с сайтов HH(обязательно)
и/или Superjob(по желанию).
Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:

Наименование вакансии.
Предлагаемую зарплату
(разносим в три поля: минимальная и максимальная и валюта).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии
(например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
Сохраните в json либо csv.
'''

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
'''
url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
           'Accept': '*/*'}
vacancy_name = input('Введите название вакансии')
page_number = 0
params = {'text': vacancy_name, 'page': page_number}
vacancy_list =[]
while page_number < 5:
    response = requests.get(url, headers=headers, params=params)
    soup = bs(response.text, 'html.parser')
    vacancies = soup.find_all('div', attrs={'class': 'vacancy-serp'})
    vacancy_data = {}
    for vacancy in vacancies:
        info = vacancy.find('a', attrs={'class': 'bloko-link'})
        name = info.getText()
        link = info['href']
        salary_info = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        salary = salary_info.getText()
        url_link = 'hh.ru'
        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['salary'] = salary
        vacancy_data['url'] = url_link
        vacancy_list.append(vacancy_data)
    page_number = page_number + 1

pprint(vacancy_list)
#Response 403 - сайт блокирует после первого запроса
'''

'''
Необходимо собрать информацию по продуктам питания с сайта: 
Список протестированных продуктов на сайте Росконтроль.рф 
Приложение должно анализировать несколько страниц сайта 
(вводим через input или аргументы).

Получившийся список должен содержать:
Наименование продукта.
Все параметры (Безопасность, Натуральность, Пищевая ценность, Качество)
Общую оценку
Сайт, откуда получена информация.
Общий результат можно вывести с помощью dataFrame через Pandas. 
Сохраните в json либо csv
'''
url = 'https://roscontrol.com'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
           'Accept': '*/*'}

category_list = []
response_category = requests.get(url + '/category/produkti/', headers=headers)
category_soup = bs(response_category.text, 'html.parser')
category_names = category_soup.find_all('a', attrs={'class': 'catalog__category-item util-hover-shadow'})
for category in category_names:
    name = category['href']
    category_list.append(name)


subcategory_list = []
for category in category_list:
    response_subcategory = requests.get(url + category, headers=headers)
    subcategory_soup = bs(response_subcategory.text, 'html.parser')
    subcategory_names = subcategory_soup.find_all('a', attrs={'class': 'catalog__category-item util-hover-shadow'})
    for subcategory in subcategory_names:
        sub_name = subcategory['href']
        subcategory_list.append(sub_name)


products_list = []
for subcategory in subcategory_list:
    response_products = requests.get(url + subcategory, headers=headers)
    products_soup = bs(response_products.text, 'html.parser')
    products_names = products_soup.find_all('a', attrs={'class': 'block-product-catalog__item js-activate-rate util-hover-shadow clear'})
    for product in products_names:
        product_name = product['href']
        products_list.append(product_name)

roscontrol_list = []
for product in products_list:
    response_list = requests.get(url + product, headers=headers)
    soup = bs(response_list.text, 'html.parser')
    items = soup.find_all('div', attrs={'class': 'product__single'})
    for item in items:
        item_dict = {}
        name = item.find('h1', attrs={'class': 'main-title testlab-caption-products util-inline-block'}).getText()
        score = item.find('div', attrs={'id': 'product__single-rev-total'}).getText().replace('\n', '').replace(
            'Общая оценка', '')
        item_dict['name'] = name
        item_dict['score'] = score
        roscontrol_list.append(item_dict)

    other_scores = soup.find_all('div', attrs={'class': 'rate-item__value'})
    score_list = []
    for other_score in other_scores:
        scores_to_list = other_score.getText().replace('\n', '')
        score_list.append(scores_to_list)

    roscontrol_list.append({'Безопасность': score_list[0], 'Натуральност': score_list[1],
                            'Пищевая ценность': score_list[2], 'Качество': score_list[3]})


pprint(score_list)

