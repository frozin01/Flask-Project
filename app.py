from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup database connection function
def get_db_connection():
    return psycopg2.connect(
        host = os.getenv('DB_HOST'),
        database = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASS'),
        port = os.getenv('DB_PORT')
    )

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory = DictCursor) as cur:
            cur.execute('SELECT id, name, price FROM products WHERE is_deleted = FALSE;')
            products = cur.fetchall()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO products (name, price, is_deleted) VALUES (%s, %s, FALSE);', (name, price))
                conn.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE products SET name = %s, price = %s WHERE id = %s;', (name, price, id))
                conn.commit()
        return redirect(url_for('index'))
    else:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT id, name, price FROM products WHERE id = %s;', (id,))
                product = cur.fetchone()
    return render_template('update_product.html', product=product)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE products SET is_deleted = TRUE WHERE id = %s;', (id,))
            conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_RUN_HOST'), port=os.getenv('FLASK_RUN_PORT'), debug=os.getenv('DEBUG'))
