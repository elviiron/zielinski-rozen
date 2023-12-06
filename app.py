from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3


app = Flask(__name__)

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

@app.route('/search', methods=['GET'])
def search_products():
    search_query = request.args.get('q')
    sort = request.args.get('sort')

    if search_query:
        try:
            return get_products(search_query, sort)
        except Exception:
            return jsonify({'error':'Something went wrong'})
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    