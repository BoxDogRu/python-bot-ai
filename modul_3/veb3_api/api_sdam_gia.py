"""
Для самостоятельного изучения
https://sdamgia.ru/
https://pypi.org/project/sdamgia-api/
https://github.com/UB-Mannheim/tesseract/wiki Tesseract installer for Windows
"""

import requests
from bs4 import BeautifulSoup
from sdamgia import SdamGIA
import random

BASE_DOMAIN = 'sdamgia.ru'
SUBJECT_BASE_URL = {
    'math': f'https://math-ege.{BASE_DOMAIN}',
    'mathb': f'https://mathb-ege.{BASE_DOMAIN}',
    'phys': f'https://phys-ege.{BASE_DOMAIN}',
    'inf': f'https://inf-ege.{BASE_DOMAIN}',
        }

# Поиск задач по предмету и слову

subject = 'math'
request = 'яблоко'
page = 1

doujin_page = requests.get(
        f'{SUBJECT_BASE_URL[subject]}/search?search={request}&page={str(page)}')
print(doujin_page.content)

soup = BeautifulSoup(doujin_page.content, 'html.parser')
print(f"Идентификаторы всех задач по математике со словом 'яблоко")
task_ids = [i.text.split()[-1] for i in soup.find_all('span', {'class': 'prob_nums'})]
print( task_ids )


# # Получение задачи по её id

id = task_ids[1]
doujin_page = requests.get(f'{SUBJECT_BASE_URL[subject]}/problem?id={id}')
soup = BeautifulSoup(doujin_page.content, 'html.parser')

probBlock = soup.find('div', {'class': 'prob_maindiv'})

for i in probBlock.find_all('img'):
    if not 'sdamgia.ru' in i['src']:
        i['src'] = SUBJECT_BASE_URL[subject] + i['src']

URL = f'{SUBJECT_BASE_URL[subject]}/problem?id={id}'

CONDITION = probBlock.find_all('div', {'class': 'pbody'})[0].text.replace('\xad', '')

ANSWER = probBlock.find('div', {'class': 'answer'}).text.replace('Ответ: ', '')
print(CONDITION)
print(ANSWER)


# Выведем список тем по математике. Выведем случайную задачу из выбранной
# пользователем темы

sdamgia = SdamGIA()
subject = 'math'
categories = sdamgia.get_catalog(subject)

for topic in categories:
    print(f"{topic['topic_name']}:")
    for category in topic['categories']:
        print(f"  {category['category_name']}: {category['category_id']}")
    print()

category_id = input('Введите идентификатор темы: ')
task_id = random.choice(sdamgia.get_category_by_id(subject, category_id))
task = sdamgia.get_problem_by_id(subject, task_id)
print("Задача:")
print(task['condition']['text'].replace('', ''))
