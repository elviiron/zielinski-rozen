from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import sqlite3


def create_database():
    connection = sqlite3.connect('product_last_my_first.db')
    cur = connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS product (title TEXT, price TEXT, img TEXT)''')
    connection.commit()
    connection.close()


def get_product_by_query(all_goods, found_goods):
    all_goods = []
    for i in found_goods:
        image = i.find('div', {"class": 'grid-product__image-wrap'})
        img = image.find('img').get('src')
        title = i.find('div', {"class": 'grid-product__title-inner'}).text.strip()
        price = i.find('div', {"class": "grid-product__price-value ec-price-item"}).text.replace("\xa0", '')
        all_goods.append((title, price, img))
    return all_goods


def insert_into_database(data):
    connection = sqlite3.connect('product_last_my_first.db')
    c = connection.cursor()
    c.executemany('INSERT INTO product VALUES (?, ?, ?)', data)
    connection.commit()
    connection.close()


def get_salt():
    all_goods = []
    driver = webdriver.Chrome()
    driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword=соль')
    driver.implicitly_wait(10)
    html = driver.execute_script("return document.body.innerHTML")
    driver.close()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})

    all_goods = get_product_by_query(all_goods, found_goods)
    create_database()
    insert_into_database(all_goods[1:])
    return all_goods

get_salt()

def get_parf():
    all_goods = []
    
    for i in range(0, 61, 60):
        driver = webdriver.Chrome()
        driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword=духи&offset={i}')
        driver.implicitly_wait(10)
        html = driver.execute_script("return document.body.innerHTML")
        driver.close()
        bsObj = BeautifulSoup(html, 'html.parser')
        found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
        all_goods += get_product_by_query(all_goods, found_goods)

    insert_into_database(all_goods[1:])
    return all_goods

get_parf()

def get_shamp():
    all_goods = []
    driver = webdriver.Chrome()
    driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword=шампунь')
    driver.implicitly_wait(10)
    html = driver.execute_script("return document.body.innerHTML")
    driver.close()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})

    all_goods = get_product_by_query(all_goods, found_goods)
    create_database()
    insert_into_database(all_goods[1:])
    return all_goods

get_shamp()

def get_svecha():
    all_goods = []
    driver = webdriver.Chrome()
    driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword=свеча')
    driver.implicitly_wait(10)
    html = driver.execute_script("return document.body.innerHTML")
    driver.close()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})

    all_goods = get_product_by_query(all_goods, found_goods)
    create_database()
    insert_into_database(all_goods[1:-2])
    return all_goods

get_svecha()

def get_skrab():
    all_goods = []
    driver = webdriver.Chrome()
    driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword=скраб')
    driver.implicitly_wait(10)
    html = driver.execute_script("return document.body.innerHTML")
    driver.close()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})

    all_goods = get_product_by_query(all_goods, found_goods)
    create_database()
    insert_into_database(all_goods[1:-1])
    return all_goods

get_skrab()

def get_ker_maska():
    all_goods = []
    driver = webdriver.Chrome()
    driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword=кератиновая+маска')
    driver.implicitly_wait(10)
    html = driver.execute_script("return document.body.innerHTML")
    driver.close()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})

    all_goods = get_product_by_query(all_goods, found_goods)
    create_database()
    insert_into_database(all_goods[1:-1])
    return all_goods

get_ker_maska()
