import requests
from bs4 import BeautifulSoup
import pprint
import json

url = 'https://irkutsk.drom.ru/toyota/land_cruiser_prado/'
response = requests.get(url)
print(response.status_code)
pprint.pprint(response.text)

# Создаем суп для разбора html
soup = BeautifulSoup(response.text, 'html.parser')

# Выбираем наименования автомобилей
vl_name = soup.findAll('h3', class_='css-16kqa8y efwtv890')
lst_name = []
for tvl in vl_name:
    lst_name.append(tvl.text)

# Выбираем характеристики
vl_har = soup.findAll('span', class_='css-1l9tp44 e162wx9x0')
lst_har = []
tr = 1
tstr = ''
for tvl in vl_har:
    tstr = tstr + tvl.text + ', '
    tr = tr + 1
    if tr == 5:
        lst_har.append(tstr[: -2])
        tstr = ''
        tr = 0
lst_har.append(tstr[: -2])

# Выбираем цену
vl_prc = soup.findAll('span', class_='css-46itwz e162wx9x0')
lst_prc = []
for tvl in vl_prc:
    lst_prc.append(tvl.text.replace('\xa0', ''))

# Формирование и вывод JSON - файла

requ = []
for itm in range(0, len(vl_name)):
    nd = {'name': lst_name[itm], 'characterictics': lst_har[itm], 'price': lst_prc[itm]}
    requ.append(nd)

to_json = [{'automobiles': requ}]

pprint.pprint(to_json)

with open('drom_requ.json', 'w') as f:
    json.dump(to_json, f)

with open('drom_requ.json') as f:
    pprint.pprint(json.loads(f.read()))
