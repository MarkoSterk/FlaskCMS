from flask import request, jsonify, current_app, url_for
from .errorController import AppError
from ..models.publicationModel import Publication
from flask_jwt_extended import current_user
from datetime import datetime
from ..utils.helperFuncs import saveImageFiles, setPostOperation
from ..utils.imageScraping import textToHtmlParser


def createOne():
    data = Publication.filterData(request.form.to_dict())

    if 'authors' in data:
        if ',' not in data['authors']:
            data['authors']=[data['authors']]
        else:
            data['authors'] = [author.strip() for author in data['authors'].split(',')]
    
    if request.files:
        data['coverImage']=saveImageFiles(request.files.getlist('coverImage'), folder='publications')[0]

    if 'text' in data: data['text']=textToHtmlParser(data['text'])

    if 'coverImage' in data:
        if data['coverImage']=='_DELETE':
            del data['coverImage'] 
    
    data['author'] = current_user._id
    data['authorName'] = current_user.name

    publication = Publication(data)
    publication.save(pre_hooks=[publication.slugify])

    return jsonify({
        'status': 'success',
        'data': [vars(publication)],
        'message': 'Publication created successfully.'
    })


def updateOne(publicationId):
    publication = Publication.findOne({'_id': publicationId})

    if publication is None:
        return AppError('Publication with this id does not exist.', 400)

    if((current_user._id != publication.author) and (current_user.role != 'admin')):
        return AppError('This is not your publication.', 401)

    data = Publication.filterData(request.form.to_dict())

    if 'authors' in data:
        if ',' not in data['authors']:
            data['authors']=[data['authors']]
        else:
            data['authors'] = [author.strip() for author in data['authors'].split(',')]
    
    if request.files:
        data['coverImage']=saveImageFiles(request.files.getlist('coverImage'), folder='publications')[0]
    
    if 'text' in data: data['text']=textToHtmlParser(data['text'])
    
    data['dateEdited'] = datetime.now().strftime("%d-%m-%Y %H:%M")

    operation = setPostOperation(data)
    publication.update(operation)
    
    return jsonify({
        'status': 'success',
        'data': [vars(publication)],
        'message': 'Publication updated successfully'
    })