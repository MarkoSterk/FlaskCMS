from flask import jsonify, request
from flask_jwt_extended import current_user

from ..controllers.errorController import AppError
from ..models.commentModel import Comment
from ..utils.helperFuncs import getQueryParameters


def addComment(parentCollection, parentId):
    data = Comment.filterData(request.form.to_dict())

    query = Comment.searchInOtherCollection(parentCollection, {'_id': parentId})
    if query is None:
        return AppError(f'Document with this ID or "{parentCollection}" collection does not exist.', 404)

    print('Here')
    data['authorName'] = current_user.name
    data['authorId'] = current_user._id
    data['parentId'] = parentId
    data['parentCollection'] = 'test'

    comment = Comment(data)
    comment.save()

    return jsonify({
        'status': 'success',
        'data': [vars(comment)],
        'message': 'Comment added successfully'
    }), 200


def editComment(commentId):
    comment = Comment.findOne({'_id': commentId})

    if comment is None:
        return AppError('Comment with this ID does not exist.', 400)
    
    if((current_user._id != comment.authorId) and (current_user.role != 'admin')):
        return AppError('This is not your comment.', 401)
    
    data = request.form.to_dict()
    if 'text' not in data:
        return AppError('You must supply a comment text.', 400)  
    
    comment.update({'$set': {'text': data['text']}})

    return jsonify({
        'status': 'success',
        'data': [vars(comment)],
        'message': 'Comment updated successfully'
    })


def getAllOf(parentId):
    queryDict = {}
    limit=0

    if request.args:
        queryDict, limit = getQueryParameters(request.args.to_dict())
        queryDict['$query']['parentId'] = parentId
    else:
        queryDict={'parentId': parentId}
    
    query = Comment.findMany(queryDict, limit)
    return jsonify({
        'status': 'success',
        'results': len(query),
        'data': [vars(q) for q in query],
        'message': 'Query completed successfully'
    }), 200


def getOne(commentId):

    comment = Comment.findOne({'_id': commentId})

    if comment is None:
        return AppError('Comment with this id does not exist.', 404)
    
    return jsonify({
        'status': 'success',
        'data': [vars(comment)],
        'message': 'Query completed successfully'
    }), 200
