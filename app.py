from flask import Flask, render_template, jsonify, request
import sqlite3
from database import create_database, insert_into_database, insert_search_query, get_products_by_query
from parser import parse_website


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('/app/database/product_last_my_first.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT DISTINCT search_query FROM search_history')
    search_history = cursor.fetchall()
    conn.close()

    return render_template('index.html', search_history=search_history)


@app.route('/search', methods=['GET'])
def search_products():
    search_query = request.args.get('q')
    sort = request.args.get('sort')
    
    if search_query:
        try:
            conn = sqlite3.connect('/app/database/product_last_my_first.db')
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


if __name__ == '__main__':
    create_database()
    app.run(host="0.0.0.0", debug=True)
    
