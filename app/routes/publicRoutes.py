from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required
from ..models.productModel import Product



publicRoutes = Blueprint('publicRoutes', __name__)


@publicRoutes.route('/', methods=['GET'])
@jwt_required()
def index():
    products = Product.findMany({'quantity': {'$gt': 0}, 'active': True})
    return render_template('public/products.html', products = products)


@publicRoutes.route('/products', methods=['GET'])
@jwt_required()
def products():
    products = Product.findMany({'quantity': {'$gt': 0}, 'active': True})
    return render_template('public/products.html', products = products)