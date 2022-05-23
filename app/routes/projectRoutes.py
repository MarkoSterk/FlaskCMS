from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..models.userModel import User
from ..models.projectModel import Project
from ..controllers import projectController
from ..controllers import handlerFactory

projectRoutes = Blueprint('projectRoutes', __name__)

@projectRoutes.route('/api/v1/projects', methods=['GET'])
def getAll():
    return handlerFactory.getAll(Project)

@projectRoutes.route('/api/v1/projects/getN', methods=['GET'])
def getN():
    return handlerFactory.getN(Project)

@projectRoutes.route('/api/v1/projects/<string:projectId>', methods=['GET'])
def getOne(projectId):
    return handlerFactory.getOne(projectId, Project,
                                populate=True,
                                populateData={
                                    'field': 'author',
                                    'model': User,
                                    'hideFields': ['password', 'passwordConfirm',
                                                    'passwordChangedAt', '_createdAt',
                                                    'active', 'confirmEmailToken']
                                })


@projectRoutes.route('/api/v1/projects/search', methods=['GET'])
def searchPosts():
    return handlerFactory.searchByQueryString(Project)


@projectRoutes.route('/api/v1/projects/<string:projectId>', methods=['DELETE'])
@jwt_required()
def deleteOne(projectId):
    return handlerFactory.deleteOne(projectId, Project)


@projectRoutes.route('/api/v1/projects', methods=['POST'])
@jwt_required()
def createOne():
    return projectController.createOne()


@projectRoutes.route('/api/v1/projects/<string:projectId>', methods=['PATCH'])
@jwt_required()
def updateOne(projectId):
    return projectController.updateOne(projectId)