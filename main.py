import csv
import json

import requests
from bs4 import BeautifulSoup

url = 'https://fitness.org.ua/tablici-bjy-i-kaloriinosti-prodyktiv-harchyvannia-na-100-gra/'
headers = {
    'accept': '*/*',
    'user_agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.5414.120 Safari/537.36',
}
req = requests.get(url, headers=headers)

with open('index.html', 'wb') as file:
    file.write(req.content)

with open('index.html', 'r', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

all_tables = soup.find_all('table')

id = 1
category_names = []
for table in all_tables:
    rep = [' ', '-', ',']
    category_name = soup.find('h2', id=f"{id}").text
    for i in rep:
        if i in category_name:
            category_name = category_name.replace(i, '_')
    category_names.append(category_name)

    table_head = soup.find(id='tablepress-106').find('tr').find_all('td')

    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbo = table_head[4].text

    with open(f'data/{id}_{category_name}.csv', 'w', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            product,
            calories,
            proteins,
            fats,
            carbo
        ))

    all_tr = table.find_all('tr')[1:]
    product_info = []
    for prod in all_tr:
        prod_data = prod.find_all('td')

        title = prod_data[0].text
        calories = prod_data[1].text
        proteins = prod_data[2].text
        fats = prod_data[3].text
        carbo = prod_data[4].text

        with open(f'data/{id}_{category_name}.csv', 'a', encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerow((
                title,
                calories,
                proteins,
                fats,
                carbo
            ))
        product_info.append({
            'title': title,
            'calories': calories,
            'proteins': proteins,
            'fats': fats,
            'carbo': carbo

        })
        with open(f'data/{id}_{category_name}.json', 'a', encoding='UTF-8') as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)

    id += 1
