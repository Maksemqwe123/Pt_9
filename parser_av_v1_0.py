import requests
from bs4 import BeautifulSoup
import time

items = []
years = []
cashed = []
urls = []

class Parser:
    def __init__(self, pages: range):
        self.pages = pages
        self.items = items
        self.years = years
        self.cashed = cashed
        self.urls = urls

        self._get_html()

    def _get_html(self):
        for page in self.pages:
            if page == 1:
                url = "https://cars.av.by/filter"
            else:
                url = f'https://cars.av.by/filter?page={page}'

            response = requests.get(url)
            # print(response.status_code)

            try:
                assert response.status_code == 200
                html_source = response.text
                self._get_info(html_source)
            except Exception as ex:
                print(f'[ERROR] {repr(ex)}')
                print(response.status_code)


    def _get_info(self, html_source):
        pages_info = BeautifulSoup(html_source, 'html.parser')

        car_names = pages_info.find_all('a', class_='listing-item__link')
        for name in car_names:
            self.items.append(name.text)
            self.urls.append(f'https://cars.av.by{name["href"]}')

        items_cashes = pages_info.find_all('div', class_='listing-item__priceusd')
        for cash in items_cashes:
            self.cashed.append(cash.text)

        years_list = pages_info.find_all('div', class_='listing-item__params')
        for year in years_list:
            self.years.append(year.text)


if __name__ == "__main__":
    parse = Parser(range(1, 2))
    all_info = zip(items, years, cashed, urls)

    for i in all_info:
        print(f'Марка: {i[0]}, год: {i[1]}, Цена: {i[2]}, Ccылка: {i[3]}')
        