from flask import request, jsonify, current_app, url_for
from .errorController import AppError
from ..models.memberModel import Member
from flask_jwt_extended import current_user
from datetime import datetime
from ..utils.helperFuncs import saveImageFiles, setPostOperation
from ..utils.imageScraping import textToHtmlParser


def createOne():    
    data = Member.filterData(request.form.to_dict())
    if request.files:
        data['image']=saveImageFiles(request.files.getlist('image'), folder='users')[0]

    if 'image' in data:
        if data['image']=='_DELETE':
            data['image']='default.jpg'

    member = Member(data)
    member.save()

    return jsonify({
        'status': 'success',
        'data': [vars(member)],
        'message': 'Member created successfully.'
    })


def updateOne(memberId):
    member = Member.findOne({'_id': memberId})

    if member is None:
        return AppError('Member with this id does not exist.', 400)

    # if(current_user.role != 'admin'):
    #     return AppError('Only admins can change members.', 401)

    data = Member.filterData(request.form.to_dict())
    
    if request.files:
        data['image']=saveImageFiles(request.files.getlist('image'), folder='users')[0]
    if 'image' in data:
        if data['image']=='_DELETE':
            data['image']='default.jpg'
    

    operation = setPostOperation(data)
    member.update(operation)
    
    return jsonify({
        'status': 'success',
        'data': [vars(member)],
        'message': 'Member updated successfully'
    })