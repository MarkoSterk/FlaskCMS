from flask import Blueprint, render_template
from ..models.productModel import Product



publicRoutes = Blueprint('publicRoutes', __name__)

@publicRoutes.route('/products', methods=['GET'])
def index():
    products = Product.findMany({'quantity': {'$gt': 0}, 'active': True})
    return render_template('public/products.html', products = products)