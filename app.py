from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_products_parf(search_query_parf):
    try:
        conn = sqlite3.connect('product_parf.db')
        conn.row_factory = sqlite3.Row
    except Exception:
        return 'Error establishing a database connection'

    query = "SELECT * FROM product WHERE title LIKE ? COLLATE utf8_bin ORDER BY CAST(REPLACE(price, ' ₽', '') AS REAL) ASC "    
    cursor = conn.execute(query, ('%' + search_query_parf.capitalize() + '%',))
    
    products_parf = cursor.fetchall()
    conn.close()

    if products_parf:
        return render_template('index.html', products=products_parf)
    else:
        return 'This product is not in the database'


@app.route('/search', methods=['GET'])
def search_products_parf():
    search_query_parf = request.args.get('q')
    if search_query_parf:
        try:
            return get_products_parf(search_query_parf)
        except Exception:
            return 'AN UNKNOWN ERROR.TRY AGAIN LATER'
    else:
        return 'YOU SHOULD WRITE THE NAME OF THE PRODUCT'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
