import requests
from bs4 import BeautifulSoup


def parse_water():
    url = 'https://www.vodokanal.mk.ua/uk/categorii/remonti'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')

    for n, i in enumerate(items, status=1):
        date = i.find('h4', class_='card-title').text.strip()
        status = i.find('h5').text
        print(f'{n}:  {date} за {status}')

    pages = soup.find('ul', class_='pagination')
    urls = []
    links = pages.find_all('a', class_='page-link')

    for link in links:
        pageNum = int(link.text) if link.text.isdigit() else None
        if pageNum != None:
            hrefval = link.get('href')
            urls.append(hrefval)

    for slug in urls:
        newUrl = url.replace('?page=1', slug)
        response = requests.get(newUrl)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')
        for n, i in enumerate(items, start=n):
            itemName = i.find('h4', class_='card-title').text.strip()
            itemPrice = i.find('h5').text
            print(f'{n}:  {date} на {status}')
