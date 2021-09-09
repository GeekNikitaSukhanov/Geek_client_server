'''
Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
'''

# API access key: a61e80be00422b844f6071c69f511455
# To get your own sign up at https://aviationstack.com/

import requests
from pprint import pprint
import json

url = 'http://api.aviationstack.com/v1/flights'
access_key = 'a61e80be00422b844f6071c69f511455'
limit = '100'
flight_status_input = input('Выберите статус рейса: \n'
                      'Запланирован - 1 \n'
                      'В небе - 2 \n'
                      'Приземлился - 3 \n'
                      'Отменен - 4 \n')

flight_status_dict = {'1': 'scheduled', '2': 'active', '3': 'landed', '4': 'cancelled'}
flight_status = flight_status_dict.get(flight_status_input)

flight_date = input('Введите дату вылета в формате YYYY-MM-DD ')
dep_iata = input('Введите код аэропорта вылета ')
arr_iata = input('Введите код аэропорта назначения ')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Accept': '*/*'}
params = {'access_key': access_key, 'flight_status': flight_status,
          'flight_data': flight_date, 'dep_iata': dep_iata, 'arr_iata': arr_iata}

response = requests.get(url, params=params, headers=headers)
j_data = response.json()

with open('airlines_data', 'w') as data:
    json.dump(j_data, data)

pprint(j_data)


