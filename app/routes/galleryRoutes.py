from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..models.userModel import User
from ..models.galleryModel import Gallery
from ..controllers import galleryController
from ..controllers import handlerFactory

galleryRoutes = Blueprint('galleryRoutes', __name__)

@galleryRoutes.route('/api/v1/galleries', methods=['GET'])
def getAll():
    return handlerFactory.getAll(Gallery)
    

@galleryRoutes.route('/api/v1/galleries/<string:galleryId>', methods=['GET'])
def getOne(galleryId):
    return handlerFactory.getOne(galleryId, Gallery,
                                populate=True,
                                populateData={
                                    'field': 'author',
                                    'model': User,
                                    'hideFields': ['password', 'passwordConfirm',
                                                    'passwordChangedAt', '_createdAt',
                                                    'active', 'confirmEmailToken']
                                })


@galleryRoutes.route('/api/v1/galleries/search', methods=['GET'])
def search():
    return handlerFactory.searchByQueryString(Gallery)


@galleryRoutes.route('/api/v1/galleries/<string:galleryId>', methods=['DELETE'])
@jwt_required()
def deleteOne(galleryId):
    return handlerFactory.deleteOne(galleryId, Gallery)


@galleryRoutes.route('/api/v1/galleries', methods=['POST'])
@jwt_required()
def createOne():
    return galleryController.createOne()


@galleryRoutes.route('/api/v1/galleries/<string:galleryId>', methods=['PATCH'])
@jwt_required()
def updateOne(galleryId):
    return galleryController.updateOne(galleryId)