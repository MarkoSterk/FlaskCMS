from flask import jsonify, request
from flask_jwt_extended import current_user
import json
from ..utils.helperFuncs import getQueryParameters

from app.controllers.errorController import AppError

def getAll(Model):
    queryDict = {}
    limit=0

    if request.args:
        queryDict, limit = getQueryParameters(request.args.to_dict())

    query = Model.findMany(queryDict, limit)
    return jsonify({
        'status': 'success',
        'results': len(query),
        'data': [vars(q) for q in query],
        'message': 'Query completed successfully'
    }), 200


def getOne(queryId, Model, populate=False, populateData = {}):
    query = Model.findOne({'_id': queryId})
    print(populate, populateData)
    if query is None:
        return AppError(f'{Model.__name__} with this ID does not exist.', 404)

    if populate:
        query.populate(populateData)
    
    print(vars(query))
    return jsonify({
        'status': 'success',
        'data': [vars(query)],
        'message': 'Query completed successfully'
    }), 200


def deleteOne(queryId, Model):
    query = Model.findOne({'_id': queryId})

    if query is None:
        return AppError(f'{Model.__name__} with this ID does not exist.', 404)
    
    if((Model.__name__ == 'Post') or (Model.__name__ == 'Publication') or (Model.__name__ == 'Project')):
        if((current_user._id != query.author) and (current_user.role != 'admin')):
            return AppError(f'This is not your {Model.__name__.lower()}.', 401)
        
    if(Model.__name__ == 'Comment'):
        if((current_user._id != query.authorId) and (current_user.role != 'admin')):
            return AppError(f'This is not your comment.', 401)
    
    if Model.__name__ == 'User':
        if((current_user._id != queryId) and (current_user.role != 'admin')):
            return AppError('This is not your profile.', 401)
    
    query.delete()
    return jsonify({
        'status': 'success',
        'data': None,
        'message': f'{Model.__name__} deleted successfully'
    }), 204


def searchByQueryString(Model):
    queryData=request.args.to_dict()
    queryObject = {}
    if len(queryData)!=0:
        queryObject = {
            '$or': [{key: {'$regex': queryData[key]}} for key in queryData]
        }
    
    queryObject['active']=True

    #print(queryObject)
    query = Model.findMany(queryObject)
    return jsonify({
        'status': 'success',
        'results': 0,
        'data': [vars(q) for q in query],
        'message': 'Query completed successfully.'
    })