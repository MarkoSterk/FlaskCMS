from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..models.userModel import User
from ..models.productModel import Product
from ..controllers import productController
from ..controllers import handlerFactory

productRoutes = Blueprint('productRoutes', __name__)

@productRoutes.route('/api/v1/products', methods=['GET'])
def getAll():
    return handlerFactory.getAll(Product)
    

@productRoutes.route('/api/v1/products/<string:productId>', methods=['GET'])
def getOne(productId):
    return handlerFactory.getOne(productId, Product,
                                populate=True,
                                populateData={
                                    'field': 'author',
                                    'model': User,
                                    'hideFields': ['password', 'passwordConfirm',
                                                    'passwordChangedAt', '_createdAt',
                                                    'active', 'confirmEmailToken']
                                })


@productRoutes.route('/api/v1/products/search', methods=['GET'])
def search():
    return handlerFactory.searchByQueryString(Product)


@productRoutes.route('/api/v1/products/<string:productId>', methods=['DELETE'])
@jwt_required()
def deleteOne(productId):
    return handlerFactory.deleteOne(productId, Product)


@productRoutes.route('/api/v1/products', methods=['POST'])
@jwt_required()
def createOne():
    return productController.createOne()


@productRoutes.route('/api/v1/products/<string:productId>', methods=['PATCH'])
@jwt_required()
def updateOne(productId):
    return productController.updateOne(productId)