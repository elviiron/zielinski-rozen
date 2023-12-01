from bs4 import BeautifulSoup
from selenium import webdriver
from database import Database
import sqlite3


class Search:
    def __init__(self, query, offset):
        self.query = query
        self.offset = offset
        self.driver = webdriver.Chrome()


    def search(self):
        self.driver.get(
            f'https://zielinskiandrozen.ru/magazin/search/?keyword={self.query}&offset={self.offset}')
        self.driver.implicitly_wait(10)
        html = self.driver.execute_script("return document.body.innerHTML")
        self.driver.close()

        bsObj = BeautifulSoup(html, 'html.parser')
        found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
        all_goods = []

        for i in found_goods:
            image = i.find('div', {"class": 'grid-product__image-wrap'})
            img = image.find('img').get('src')
            title = i.find('div', {"class": 'grid-product__title-inner'}).text.strip()
            price = i.find('div', {"class": "grid-product__price-value ec-price-item"}).text.replace("\xa0", '')

            all_goods.append((title, price, img))

        return all_goods


def get_all_products(query):
    all_goods = []
    offset = 0
    while True:
        scraper = Search(query, offset)
        goods = scraper.search()
        all_goods.extend(goods)
        if len(goods) < 60:
            break
        offset += 60

    db = Database()
    db.create_table_parf()
    db.insert_data_parf(all_goods)
    db.close_connection()

    return all_goods

get_all_products('соль')

