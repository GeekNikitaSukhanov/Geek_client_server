'''
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
для конкретного пользователя, сохранить JSON-вывод в файле *.json.
'''

import requests
import json
from pprint import pprint

url = 'https://api.github.com/users/GeekNikitaSukhanov/repos'
my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
              'Accept': '*/*'}

response = requests.get(url)

j_data = response.json()

j_dict = {}
counter = 1
for i in j_data:
    temp_dict = {counter: i.get('name')}
    j_dict.update(temp_dict)
    counter = counter + 1

with open('repo_data', 'w') as data:
    json.dump(j_dict, data)


pprint(j_dict)
