from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..models.userModel import User
from ..models.publicationModel import Publication
from ..controllers import publicationController
from ..controllers import handlerFactory

publicationRoutes = Blueprint('publicationRoutes', __name__)

@publicationRoutes.route('/api/v1/publications', methods=['GET'])
def getAll():
    return handlerFactory.getAll(Publication)

@publicationRoutes.route('/api/v1/publications/getN', methods=['GET'])
def getN():
    return handlerFactory.getN(Publication)

@publicationRoutes.route('/api/v1/publications/<string:publicationId>', methods=['GET'])
def getOne(publicationId):
    return handlerFactory.getOne(publicationId, Publication,
                                populate=True,
                                populateData={
                                    'field': 'author',
                                    'model': User,
                                    'hideFields': ['password', 'passwordConfirm',
                                                    'passwordChangedAt', '_createdAt',
                                                    'active', 'confirmEmailToken']
                                })


@publicationRoutes.route('/api/v1/publications/search', methods=['GET'])
def searchPosts():
    return handlerFactory.searchByQueryString(Publication)


@publicationRoutes.route('/api/v1/publications/<string:publicationId>', methods=['DELETE'])
@jwt_required()
def deleteOne(publicationId):
    return handlerFactory.deleteOne(publicationId, Publication)


@publicationRoutes.route('/api/v1/publications', methods=['POST'])
@jwt_required()
def createOne():
    return publicationController.createOne()


@publicationRoutes.route('/api/v1/publications/<string:publicationId>', methods=['PATCH'])
@jwt_required()
def updateOne(publicationId):
    return publicationController.updateOne(publicationId)