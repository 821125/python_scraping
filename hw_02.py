import json
import requests
import re
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd


url = 'https://voronezh.hh.ru'

search_text = 'Python'

params = {
    'clusters': 'true',
    'order_clusters': 'true',
    'st': 'searchVacancy',
    'text': 'Python',
    'area': '268'
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/93.0.4577.82 Safari/537.36'}

url_link = '/search/vacancy'
vacancy_number = 1
page = 0


def isint(arg):
    return bool(arg.isdigit())


while True:

    response = requests.get(url + url_link, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    button_next = soup.find('a', text='дальше')
    jobs = []

    for vacancy in vacancy_list:

        vacancy_data = {}
        vacancy_name_info = vacancy.find('a', attrs={'class': 'bloko-link'})
        vacancy_name = vacancy_name_info.text
        vacancy_link = vacancy_name_info['href']
        vacancy_employer = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})

        if not vacancy_employer:
            vacancy_employer = None
        else:
            vacancy_employer = vacancy_employer.text

        vacancy_city = vacancy.find('span', attrs={'class': 'vacancy-serp-item__meta-info'}).text
        salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})

        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = salary.getText().replace(u'\xa0', u'')
            salary = re.split(r'\s|<|>', salary)

            if salary[0] == 'до':
                salary_min = None
                if isint(salary[1]) and isint(salary[2]):
                    salary_max = int(''.join([salary[1], salary[2]]))
                    salary_currency = salary[3]
                else:
                    salary_max = int(salary[1])
                    salary_currency = salary[2]
            elif salary[0] == 'от':
                if isint(salary[1]) and isint(salary[2]):
                    salary_min = int(''.join([salary[1], salary[2]]))
                    salary_currency = salary[3]
                else:
                    salary_min = int(salary[1])
                    salary_currency = salary[2]
                salary_max = None
            else:
                if isint(salary[0]) and isint(salary[1]):
                    salary_min = int(''.join([salary[0], salary[1]]))
                    if isint(salary[3]) and isint(salary[4]):
                        salary_max = int(''.join([salary[3], salary[4]]))
                        salary_currency = salary[5]
                    else:
                        salary_max = int(salary[3])
                        salary_currency = salary[4]
                else:
                    salary_min = int(salary[0])
                    if isint(salary[2]) and isint(salary[3]):
                        salary_max = int(''.join([salary[2], salary[3]]))
                        salary_currency = salary[4]
                    else:
                        salary_max = int(salary[2])
                        salary_currency = salary[3]

        vacancy_data['vacancy_number'] = vacancy_number
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['employer'] = vacancy_employer
        vacancy_data['city'] = vacancy_city
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency
        vacancy_data['site'] = url

        vacancy_number += 1
        jobs.append(vacancy_data)

    if not button_next or not response.ok:
        break

    page += 1
    params = {
        'clusters': 'true',
        'order_clusters': 'true',
        'st': 'searchVacancy',
        'text': 'Python',
        'area': '268',
        'page': page
    }

    with open('jobs.json', 'w') as json_file:
        json.dump(jobs, json_file)

# pprint(jobs)

data = pd.read_json('jobs.json')
df = pd.DataFrame(data)

pprint(df)
