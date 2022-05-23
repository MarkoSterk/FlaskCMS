from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..models.memberModel import Member
from ..controllers import memberController
from ..controllers import handlerFactory

memberRoutes = Blueprint('memberRoutes', __name__)

@memberRoutes.route('/api/v1/members', methods=['GET'])
def getAll():
    return handlerFactory.getAll(Member)

@memberRoutes.route('/api/v1/members/getN', methods=['GET'])
def getN():
    return handlerFactory.getN(Member)

@memberRoutes.route('/api/v1/members/<string:memberId>', methods=['GET'])
def getOne(memberId):
    return handlerFactory.getOne(memberId, Member,
                                populate=False)


@memberRoutes.route('/api/v1/members/search', methods=['GET'])
def search():
    return handlerFactory.searchByQueryString(Member)


@memberRoutes.route('/api/v1/members/<string:memberId>', methods=['DELETE'])
@jwt_required()
def deleteOne(memberId):
    return handlerFactory.deleteOne(memberId, Member)


@memberRoutes.route('/api/v1/members', methods=['POST'])
@jwt_required()
def createOne():
    return memberController.createOne()


@memberRoutes.route('/api/v1/members/<string:memberId>', methods=['PATCH'])
@jwt_required()
def updateOne(memberId):
    return memberController.updateOne(memberId)