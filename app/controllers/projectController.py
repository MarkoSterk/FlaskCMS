from flask import request, jsonify, current_app, url_for
from .errorController import AppError
from ..models.projectModel import Project
from flask_jwt_extended import current_user
from datetime import datetime
from ..utils.helperFuncs import saveImageFiles, setPostOperation
from ..utils.imageScraping import textToHtmlParser


def createOne():
    data = request.form.to_dict()
    
    data = Project.filterData(data)
    if request.files:
        data['coverImage']=saveImageFiles(request.files.getlist('coverImage'), folder='projects')[0]

    if 'text' in data: data['text']=textToHtmlParser(data['text'])
    if 'textSlo' in data: data['textSlo']=textToHtmlParser(data['textSlo'])

    if 'tags' in data:
        data['tags'] = data['tags'].split(',') if ',' in data['tags'] else [data['tags']]

    if 'coverImage' in data:
        if data['coverImage']=='_DELETE':
            del data['coverImage'] 

    data['author'] = current_user._id
    data['authorName'] = current_user.name

    project = Project(data)
    project.save(pre_hooks=[project.slugify])

    return jsonify({
        'status': 'success',
        'data': [vars(project)],
        'message': 'Project created successfully.'
    })


def updateOne(projectId):
    project = Project.findOne({'_id': projectId})

    if project is None:
        return AppError('Project with this id does not exist.', 400)

    if((current_user._id != project.author) and (current_user.role != 'admin')):
        return AppError('This is not your project.', 401)

    data = Project.filterData(request.form.to_dict())
    
    if request.files:
        data['coverImage']=saveImageFiles(request.files.getlist('coverImage'), folder='projects')[0]
    
    data['dateEdited'] = datetime.now().strftime("%d-%m-%Y %H:%M")
    
    if 'text' in data: data['text']=textToHtmlParser(data['text'])
    if 'textSlo' in data: data['textSlo']=textToHtmlParser(data['textSlo'])

    if 'tags' in data:
        data['tags'] = data['tags'].split(',') if ',' in data['tags'] else [data['tags']]

    operation = setPostOperation(data)
    project.update(operation)
    
    return jsonify({
        'status': 'success',
        'data': [vars(project)],
        'message': 'Project updated successfully'
    })