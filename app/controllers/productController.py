from email.mime import image
from flask import request, jsonify, current_app
from .errorController import AppError
from ..models.productModel import Product
from flask_jwt_extended import current_user
from datetime import datetime
from ..utils.helperFuncs import saveImageFiles, setPostOperation
from ..utils.imageScraping import textToHtmlParser


def createOne():
    data = request.form.to_dict()
    if request.files:
        data['images']=[saveImageFiles(request.files.getlist(key), folder='products')[0] for key in request.files.to_dict()]
    
    if 'text' in data: data['text']=textToHtmlParser(data['text'])

    data=Product.filterData(data)

    data['author'] = current_user._id

    product = Product(data)
    product.save(pre_hooks=[product.slugify])

    return jsonify({
        'status': 'success',
        'data': [vars(product)],
        'message': 'Product created successfully.'
    })


def updateOne(productId):
    product=Product.findOne({'_id': productId})
    if product is None:
        return AppError('Product with this id does not exist', 400)
    
    if((current_user._id != product.author) and (current_user.role != 'admin')):
        return AppError('This is not your product.', 401)

    data = request.form.to_dict()

    data['images']=[]
    for key in data:
        if 'oldImage_' in str(key):
            data['images'].append(data[key])
    
    newFiles=[]
    if request.files:
        newFiles=[saveImageFiles(request.files.getlist(key), folder='products')[0] for key in request.files.to_dict()]
        data['images'].extend(newFiles)
    
    if 'text' in data: data['text']=textToHtmlParser(data['text'])

    data=Product.filterData(data)
    operation = setPostOperation(data)
    product.update(operation)

    return jsonify({
        'status': 'success',
        'data': [vars(product)],
        'message': 'Product updated successfully.'
    })