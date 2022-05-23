from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controllers import commentController
from ..controllers import handlerFactory
from ..models.commentModel import Comment

commentRoutes = Blueprint('commentRoutes', __name__)

@commentRoutes.route('/api/v1/comments/<string:parentCollection>/<string:parentId>', methods=['POST'])
@jwt_required()
def addComment(parentCollection, parentId):
    return commentController.addComment(parentCollection, parentId)


@commentRoutes.route('/api/v1/comments/<string:commentId>', methods=['DELETE'])
@jwt_required()
def deleteComment(commentId):
    return handlerFactory.deleteOne(commentId, Comment)


@commentRoutes.route('/api/v1/comments/<string:commentId>', methods=['PATCH'])
@jwt_required()
def editComment(commentId):
    return commentController.editComment(commentId)


@commentRoutes.route('/api/v1/comments/all', methods=['GET'])
def getAll():
    return handlerFactory.getAll(Comment)


@commentRoutes.route('/api/v1/comments/allof/<string:parentId>', methods=['GET'])
def getAllOf(parentId):
    return commentController.getAllOf(parentId)


@commentRoutes.route('/api/v1/comments/one/<string:commentId>', methods=['GET'])
def getOne(commentId):
    return commentController.getOne(commentId)
