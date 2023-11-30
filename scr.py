from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3


def create_database():
    connection = sqlite3.connect('product_parf.db')
    cur = connection.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS product                 
                   (title TEXT, price TEXT, img TEXT)''')

    connection.commit()
    connection.close()


def get_product_by_query(query, offset):
    driver = webdriver.Chrome()
    driver.get(f'https://zielinskiandrozen.ru/magazin/search/?keyword={query}&offset={offset}')
    driver.implicitly_wait(10)
    html = driver.execute_script("return document.body.innerHTML")
    driver.close()

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


def insert_into_database(data):
    connection = sqlite3.connect('product_parf.db')
    c = connection.cursor()
    c.executemany('INSERT INTO product VALUES (?, ?, ?)', data)

    connection.commit()
    connection.close()


def get_all_products_by_query(query):
    all_goods = []
    offset = 0
    while True:
        goods = get_product_by_query(query, offset)
        all_goods.extend(goods)
        if len(goods) < 60:
            break
        offset += 60

    create_database()
    insert_into_database(all_goods)
    return all_goods

get_all_products_by_query('мыльница')

