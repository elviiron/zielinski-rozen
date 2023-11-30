from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_products(search_query):
    conn = sqlite3.connect('product_parf.db')
    conn.row_factory = sqlite3.Row
    query = "SELECT * FROM product WHERE title LIKE ? COLLATE utf8_bin ORDER BY CAST(REPLACE(price, ' ₽', '') AS REAL) ASC "    
    cursor = conn.execute(query, ('%' + search_query.capitalize() + '%',))
    
    products = cursor.fetchall()
    conn.close()
    if products:
        return render_template('./index.html', products=products)
    else:
        return 'TRY AGAIN, SUNNY!'


@app.route('/search', methods=['GET'])
def search_products():
    search_query = request.args.get('q')
    if search_query:
        try:
            return get_products(search_query)
        except Exception:
            return jsonify({'error':'Something went wrong'})
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
