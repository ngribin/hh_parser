import requests
from  bs4 import BeautifulSoup
import lxml
import fake_useragent
import time
import json

def get_link(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f'https://nn.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text={text}&page=1&hhtmFrom=vacancy_search_list',
        headers =  {'user-agent': ua.random}
    )

    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content,'lxml')

    try:
        page_count = int(soup.find('div', attrs={'class': 'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)
    except:
        return

    for page in range(page_count):
        try:
            data = requests.get(
                url=f'https://nn.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text={text}&page={page}&hhtmFrom=vacancy_search_list',
                headers={'user-agent': ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, 'lxml')
            for a in soup.find_all('a', attrs={'class':'serp-item__title'}):
                yield f'{a.attrs["href"].split("?")[0]}'
        except Exception as e:
            print(f"{e}")
        time.sleep(1)


def get_resume(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={'user-agent': ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:

        company = soup.find(attrs={'class':'vacancy-company-name'}).text
        expirience = soup.find(attrs={'data-qa': 'vacancy-experience'}).text
        viewers = soup.find(attrs={'class': 'vacancy-viewers-count'}).text.replace('\xa0', ' ')
        name = soup.find(attrs={'class': 'vacancy-title'}).text


    except:
        name = ''
        company = ''
        viewers = ''
        expirience = ''

    try:
        tags = [tag.text for tag in soup.find(attrs={'class':"bloko-tag-list"}).find_all(attrs={'class': 'bloko-tag bloko-tag_inline'})]
    except:
        tags = []

    try:
        reguire = [reg.text for reg in soup.find(attrs={'class':"vacancy-description"}).find('div', attrs={'class': "l-paddings b-vacancy-desc"}).find_all('li')]
    except:
        reguire = []


    resume = {

        'company': company,
        'expirince': expirience,
        'tags': tags,
        'viewers': viewers,
        'name': name,
        'requiremnts': reguire,
    

    }
    return resume



if __name__ == '__main__':
    # for a in get_link('data science'):
    #     print(get_resume(a))
    #     time.sleep(1)

    data = []
    for a in get_link('data scientist'):
        data.append(get_resume(a))
        time.sleep(1)
        with open('ds.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)