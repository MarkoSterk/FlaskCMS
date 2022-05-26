from email.mime import image
from flask import request, jsonify, current_app, url_for
from .errorController import AppError
from ..models.galleryModel import Gallery
from flask_jwt_extended import current_user
from datetime import datetime
from ..utils.helperFuncs import saveImageFiles, setPostOperation
from ..utils.imageScraping import textToHtmlParser


def createOne():
    data = request.form.to_dict()
    
    if request.files:
        data['images']=[saveImageFiles(request.files.getlist(key), folder='galleries')[0] for key in request.files.to_dict()]

    if 'coverImage' in data:
        data['coverImage']=data['images'][list(request.files.to_dict().keys()).index(data['coverImage'])]
    
    if 'text' in data: data['text']=textToHtmlParser(data['text'])

    if 'tags' in data:
        data['tags'] = data['tags'].split(',') if ',' in data['tags'] else [data['tags']]

    data=Gallery.filterData(data)

    data['author'] = current_user._id
    data['authorName'] = current_user.name

    gallery = Gallery(data)
    gallery.save(pre_hooks=[gallery.slugify])

    return jsonify({
        'status': 'success',
        'data': [vars(gallery)],
        'message': 'Gallery created successfully.'
    })


def updateOne(galleryId):
    gallery=Gallery.findOne({'_id': galleryId})
    if gallery is None:
        return AppError('Gallery with this id does not exist', 400)
    
    if((current_user._id != gallery.author) and (current_user.role != 'admin')):
        return AppError('This is not your gallery.', 401)

    data = request.form.to_dict()

    data['images']=[]
    for key in data:
        if 'oldImage_' in str(key):
            data['images'].append(data[key])
    
    newFiles=[]
    if request.files:
        newFiles=[saveImageFiles(request.files.getlist(key), folder='galleries')[0] for key in request.files.to_dict()]
        data['images'].extend(newFiles)
    
    print(data)
    if 'coverImage' in data:
        if 'old_' in data['coverImage']:
            data['coverImage']=data['coverImage'].split('_')[1]
        elif(newFiles):
            data['coverImage']=newFiles[list(request.files.to_dict().keys()).index(data['coverImage'])]
        else:
            del data['coverImage']
    else:
        delattr(gallery, 'coverImage')
    
    if 'text' in data: data['text']=textToHtmlParser(data['text'])

    if 'tags' in data:
        data['tags'] = data['tags'].split(',') if ',' in data['tags'] else [data['tags']]

    data=Gallery.filterData(data)
    operation = setPostOperation(data)
    gallery.update(operation)

    return jsonify({
        'status': 'success',
        'data': [vars(gallery)],
        'message': 'Gallery updated successfully.'
    })