import json
from app import app, db
import os
from sqlalchemy import or_
from app.models import Category, Product, User, Receipt, ReceiptDetail
from flask_login import current_user
import hashlib


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_categories():
    return Category.query.all()
    #return read_json(os.path.join(app.root_path, 'data/categories.json'))

def load_products(cate_id=None, kw = None, from_price = None, to_price = None, page = 1):
    products = Product.query.filter(Product.active.__eq__(True))
    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if kw:
        products = products.filter(or_(Product.name.ilike(f"%{kw}%")))
        #products = products.filter(Product.name.__contains__(kw))
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size


    return products.slice(start, end).all()
    # products = read_json(os.path.join(app.root_path, 'data/products.json'))
    #
    # if cate_id:
    #     products = [p for p in products if p['category_id'] == int(cate_id)]
    #
    # if kw:
    #     products = [p for p in products if p['name'].lower().find(kw.lower()) >= 0]
    #
    # if from_price:
    #     products = [p for p in products if p['price'] >= float(from_price)]
    #
    # if to_price:
    #     products = [p for p in products if p['price'] <= float(to_price)]
    #
    # return products

def count_products():
    return Product.query.filter(Product.active.__eq__(True)).count()

def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()
def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)
def get_product_by_id(product_id):
    return Product.query.get(product_id)

def add_receipt(cart):
    if cart:
        try:
            receipt = Receipt(user=current_user)
            db.session.add(receipt)


            for c in cart.values():
                d = ReceiptDetail(receipt=receipt,
                                  product_id=c['id'],
                                  quantity=c['quantity'],
                                  unit_price=c['price'])
                db.session.add(d)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(f"Error adding receipt: {str(ex)}")
def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }
