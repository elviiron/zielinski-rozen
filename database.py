import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('product_parf.db')
        self.cursor = self.connection.cursor()


    def create_table_parf(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS product
                            (title TEXT, price TEXT, img TEXT)''')
        self.connection.commit()


    def insert_data_parf(self, data):
        self.cursor.executemany('INSERT INTO product VALUES (?, ?, ?)', data)
        self.connection.commit()


    def close_connection(self):
        self.connection.close()

