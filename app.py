from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from models import Product
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    
    db.init_app(app)

    # with app.app_context():
    #     db.create_all()
    
    @app.route('/')
    def index():
        products = Product.query.filter_by(is_deleted=False).all()
        return render_template('index.html', products=products)

    @app.route('/add', methods=['GET', 'POST'])
    def add_product():
        if request.method == 'POST':
            name = request.form['name']
            price = request.form['price']
            new_product = Product(name=name, price=price)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('add_product.html')

    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update_product(id):
        product = Product.query.get_or_404(id)
        if request.method == 'POST':
            product.name = request.form['name']
            product.price = request.form['price']
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('update_product.html', product=product)

    @app.route('/delete/<int:id>', methods=['GET', 'POST'])
    def delete_product(id):
        product = Product.query.get_or_404(id)
        product.is_deleted = True
        db.session.commit()
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=os.getenv('FLASK_RUN_HOST'), port=os.getenv('FLASK_RUN_PORT'), debug=os.getenv('DEBUG'))
