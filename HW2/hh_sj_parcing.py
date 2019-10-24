import requests
from bs4 import BeautifulSoup as bs
from lxml import html
from pprint import pprint
import urllib.parse as urllib
import pandas as pd
import time


def get_html(url_, user_agent_):
    html_ = requests.get(url_, headers=user_agent_)
    print('Парсинг страницы --> ', url_)
    return html_.text


def read_write_file(data_, file_name, operation, encoding):
    with open(file_name, operation, encoding=encoding) as file:
        if operation == 'r':
            data_ = file.read()
            file.close()
            return data_
        else:
            file.write(data_)
            file.close()
            return


# ### Вводимые аргументы -----------
# ### ------------------------------
# job_title = 'детский врач'
# job_title = 'Продавец-кассир'
# job_title = 'Секретарь'
job_title = 'Помощник руководителя'
hh_area = '1' # Москва
sj_area = '4' # Москва
pages = 3
use_requests = True
# ### ------------------------------

hh_site_url = 'https://hh.ru'
sj_site_url = 'https://www.superjob.ru'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.107'}
hh_file_base = 'hh_html'
sj_file_base = 'sj_html'
hh_main_link = hh_site_url + '/search/vacancy'
sj_main_link = sj_site_url + '/vacancy/search/'
hh_job_title = job_title
sj_job_title = job_title
if len(job_title.split()) > 1:
    hh_job_title = '+'.join(job_title.split())
    sj_job_title = '%20'.join(job_title.split())

while use_requests:
    hh_link_base = hh_main_link + '?text=' + hh_job_title + '&area=' + hh_area + '&page='
    sj_link_base = sj_main_link + '?keywords=' + sj_job_title + '&geo[t][0]=' + sj_area + '&page='
    for p in range(pages):
        hh_link = hh_link_base + str(p)
        sj_link = sj_link_base + str(p)
        hh_one_page_html = get_html(hh_link, header)
        sj_one_page_html = get_html(sj_link, header)
        hh_file = hh_file_base + str(p) + '.html'
        sj_file = sj_file_base + str(p) + '.html'
        read_write_file(hh_one_page_html, hh_file, 'w', 'utf-8')
        read_write_file(sj_one_page_html, sj_file, 'w', 'utf-8')
        time.sleep(5)
    break
hh_data = dict()
for p in range(pages):
    hh_file = hh_file_base + str(p) + '.html'
    one_page_html = read_write_file(None, hh_file, 'r', 'utf-8')
    parsed_html = bs(one_page_html, 'lxml')
    vacancy_divs = parsed_html.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
    for vacancy in vacancy_divs:
        link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})
        url = link.get('href')
        vacancy_id = urllib.urlparse(url).path.split('/')[2]
        main_info = vacancy.findChildren(recursive=False)
        title = main_info[0].getText()
        s_txt = main_info[1].getText()
        s_min = None
        s_max = None
        if s_txt:
            dash = s_txt.find('-')
            if dash != -1:
                s_txt = s_txt.split()
                s1 = s_txt[1].split('-')
                s_txt.pop(1)
                s_txt.insert(1, s1[0])
                s_txt.insert(2, s1[1])
                s_min = s_txt[0] + s_txt[1]
                s_max = s_txt[2] + s_txt[3]
            else:
                s_txt = s_txt.split()
            for i in range(len(s_txt)):
                if s_txt[i] == 'от':
                    s_min = s_txt[i+1] + s_txt[i+2]
                    s_max = None
                    break
                if s_txt[i] == 'до':
                    s_max = s_txt[i + 1] + s_txt[i + 2]
                    s_min = None
                    break

        hh_data[vacancy_id] = list()
        hh_data[vacancy_id].append(title)
        hh_data[vacancy_id].append(s_min)
        hh_data[vacancy_id].append(s_max)
        hh_data[vacancy_id].append(url)
        hh_data[vacancy_id].append(hh_site_url[8:])
# pprint(hh_data)
# pprint(len(hh_data))
sj_data = dict()
for p in range(pages):
    sj_file = sj_file_base + str(p) + '.html'
    one_page_html = read_write_file(None, sj_file, 'r', 'utf-8')
    parsed_html = bs(one_page_html, 'lxml')
    vacancy_divs = parsed_html.find_all('div', {'class': '_2g1F-'})
    salary = []
    links = []
    for vacancy in vacancy_divs:
        link = vacancy.find('a', {'class': '_3dPok'})
        s_min = None
        s_max = None
        if link:
            links.append(link)
            s_txt = vacancy.find('span', {'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})
            salary.append(s_txt)
            if links.count(link) > 1:
                links.pop()
                salary.pop()
            title = links[-1].getText()
            if title.find('У компании есть ещё') != -1:
                links.pop()
                salary.pop()
            url = sj_site_url + links[-1].get('href')
            vacancy_id = urllib.urlparse(url).path.split('-')[-1][:-5]
            title = links[-1].getText()
            s = salary[-1].getText()
            dash = s.find('-')
            if dash != -1:
                s = s.split()
                s_min = s[0] + s[1]
                s_max = s[3] + s[4]
            else:
                s = s.split()
            if s[0] == 'По':
                s_min = None
                s_max = None
            if s[0] == 'от':
                s_min = s[1] + s[2]
                s_max = None
            if s[0] == 'до':
                s_min = None
                s_max = s[1] + s[2]
            sj_data[vacancy_id] = list()
            sj_data[vacancy_id].append(title)
            sj_data[vacancy_id].append(s_min)
            sj_data[vacancy_id].append(s_max)
            sj_data[vacancy_id].append(url)
            sj_data[vacancy_id].append(sj_site_url[8:])
# pprint(sj_data)
# pprint(len(sj_data))
data = dict(list(hh_data.items()) + list(sj_data.items()))
pprint(data)
print(f'Общее количество вакансий по ключевому слову "{job_title}" = {len(data)}')
