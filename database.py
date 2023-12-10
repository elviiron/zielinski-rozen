import sqlite3
import config

def create_database():
    connection = sqlite3.connect(config.database_name)
    cur = connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS product (s_query TEXT, title TEXT, price TEXT, img TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS search_history (search_query TEXT, products TEXT)''')
    connection.commit()
    connection.close()


def insert_into_database(data):
    connection = sqlite3.connect(config.database_name)
    c = connection.cursor()
    c.executemany('INSERT INTO product VALUES (?, ?, ?, ?)', data)
    connection.commit()
    connection.close()


def insert_search_query(search_query, products):
    connection = sqlite3.connect(config.database_name)
    c = connection.cursor()
    c.execute('INSERT INTO search_history VALUES (?, ?)', (search_query, products))
    connection.commit()
    connection.close()

def get_products_by_query(search_query, sort=None):
    connection = sqlite3.connect(config.database_name)
    connection.row_factory = sqlite3.Row

    query = """SELECT * FROM product WHERE s_query = ? {}
    """.format("ORDER BY CAST(REPLACE(price, ' ₽', '') AS REAL) ASC" if sort=='asc' else "ORDER BY CAST(REPLACE(price, ' ₽', '') AS REAL) DESC" if sort=='desc' else "")
    
    cursor = connection.execute(query, (search_query,))
    products = cursor.fetchall()
    connection.close()
    return products
