<<<<<<< HEAD
from flask import Flask, render_template, jsonify, request
=======
from flask import Flask, render_template, jsonify, request, redirect, url_for
>>>>>>> ef755944522762c35f85c24d8fe79b82b1aa59f9
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver



app = Flask(__name__)

<<<<<<< HEAD

def create_database():
    connection = sqlite3.connect('product_last_my_first.db')
    cur = connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS product (s_query TEXT, title TEXT, price TEXT, img TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS search_history (search_query TEXT, products TEXT)''')
    connection.commit()
    connection.close()


def insert_into_database(data):
    connection = sqlite3.connect('product_last_my_first.db')
    c = connection.cursor()
    c.executemany('INSERT INTO product VALUES (?, ?, ?, ?)', data)
    connection.commit()
    connection.close()


def insert_search_query(search_query, products):
    connection = sqlite3.connect('product_last_my_first.db')
    c = connection.cursor()
    c.execute('INSERT INTO search_history VALUES (?, ?)', (search_query, products))
    connection.commit()
    connection.close()


def get_products_by_query(search_query, sort=None):
    connection = sqlite3.connect('product_last_my_first.db')
    connection.row_factory = sqlite3.Row

    query = """SELECT * FROM product WHERE s_query = ? {}
    """.format("ORDER BY CAST(REPLACE(price, ' ₽', '') AS REAL) ASC" if sort=='asc' else "ORDER BY CAST(REPLACE(price, ' ₽', '') AS REAL) DESC" if sort=='desc' else "")
    
    cursor = connection.execute(query, (search_query,))
    products = cursor.fetchall()
    connection.close()
    return products


def get_product_by_query(search_query, all_goods, found_goods):
    for i in found_goods:
        image = i.find('div', {"class": 'grid-product__image-wrap'})
        img = image.find('img').get('src')
        title = i.find('div', {"class": 'grid-product__title-inner'}).text.strip()
        price = i.find('div', {"class": "grid-product__price-value ec-price-item"}).text.replace("\xa0", '')
        all_goods.append((search_query, title, price, img))
    return all_goods


def parse_website(search_query):
    all_goods = []
    driver = webdriver.Chrome()
    driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword={search_query}')
    driver.implicitly_wait(10)
    html = driver.execute_script("return document.body.innerHTML")
    driver.close()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
    number = int(bsObj.find('div', {"class": "ec-breadcrumbs"}).text.replace("Магазин/Поиск: нашлось ", ''))
    print(number)

    if number > 60 and number < 120:
        for i in range(0, 61, 60):
            driver = webdriver.Chrome()
            driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword={search_query}&offset={i}')
            driver.implicitly_wait(10)
            html = driver.execute_script("return document.body.innerHTML")
            driver.close()
            bsObj = BeautifulSoup(html, 'html.parser')
            found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
            all_goods = get_product_by_query(search_query, all_goods, found_goods)

    elif number > 120:
        for i in range(0, 121, 60):
            driver = webdriver.Chrome()
            driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword={search_query}&offset={i}')
            driver.implicitly_wait(10)
            html = driver.execute_script("return document.body.innerHTML")
            driver.close()
            bsObj = BeautifulSoup(html, 'html.parser')
            found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
            all_goods = get_product_by_query(search_query, all_goods, found_goods)

    else:
        driver = webdriver.Chrome()
        driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword={search_query}')
        driver.implicitly_wait(10)
        html = driver.execute_script("return document.body.innerHTML")
        driver.close()
        bsObj = BeautifulSoup(html, 'html.parser')
        found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
        all_goods = get_product_by_query(search_query, all_goods, found_goods)
    
    return all_goods


@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('product_last_my_first.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT DISTINCT search_query FROM search_history')
    search_history = cursor.fetchall()
    conn.close()

    return render_template('index.html', search_history=search_history)

=======
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def get_products(search_query, sort):
    conn = sqlite3.connect('product_last_my_first.db')
    conn.row_factory = sqlite3.Row
    query = """
            SELECT * FROM product 
            WHERE title LIKE ? COLLATE utf8_bin
            {}
             """.format("ORDER BY CAST(REPLACE(price, ' ₽', '') AS REAL) ASC" if sort=='asc' else "ORDER BY CAST(REPLACE(price, ' ₽', '') AS REAL) DESC" if sort=='desc' else "")

    cursor = conn.execute(query, ('%' + search_query.capitalize() + '%',))

    products = cursor.fetchall()
    conn.close()
    if products:
        return render_template('index.html', products=products)
    else:
        return 'TRY AGAIN, SUNNY!'
>>>>>>> ef755944522762c35f85c24d8fe79b82b1aa59f9

@app.route('/search', methods=['GET'])
def search_products():
    search_query = request.args.get('q')
    sort = request.args.get('sort')
<<<<<<< HEAD
    
    if search_query:
        try:
            conn = sqlite3.connect('product_last_my_first.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT products FROM search_history WHERE search_query = ?', (search_query,))
            products = cursor.fetchone()
            conn.close()

            if products:
                product_list = products['products'].split(',')
                return render_template('index.html', products=get_products_by_query(search_query, sort), search_query=search_query, product_list= product_list)
            else:
                all_goods = parse_website(search_query)
                insert_into_database(all_goods[1:])
                insert_search_query(search_query, ','.join([item[1] for item in all_goods[1:]]))
                return render_template('index.html', products=all_goods, search_query=search_query, product_list=[item[1] for item in all_goods[1:]], sort=sort)
        
        except Exception as excep:
            print('Error:', excep)
        
    return render_template('index.html')
=======
>>>>>>> ef755944522762c35f85c24d8fe79b82b1aa59f9

    if search_query:
        try:
            return get_products(search_query, sort)
        except Exception:
            return jsonify({'error':'Something went wrong'})
    else:
        return jsonify([])

if __name__ == '__main__':
    create_database()
    app.run(host="0.0.0.0", debug=True)
    