from app import bcrypt
import secrets
from flask import current_app
import os
from PIL import Image
import json

"""
Helper functions which can be used across the app. 

hashUrlSafe: creates a URL safe hashed string

saveImageFiles: saves image files from a form into the static folder and asignes
random string names (it keeps the provided extension) but it only accepts provided
image formats (allowed_formats). Default: allowed_formats=['png', 'jpg', 'jpeg', 'bmp']
"""

def getQueryParameters(args):
    queryDict = {}
    limit=0

    if '$orderby' in args:
        queryDict['$orderby']=json.loads(args['$orderby'])
        del args['$orderby']
    
    if 'limit' in args:
        limit=int(args['limit'])
        del args['limit']

    for key in args:
        args[key]=json.loads(args[key])
    queryDict['$query']=args

    return queryDict, limit


def hashUrlSafe(stringToHash):
    hashed_string = '/'
    while True:
        if '/' in hashed_string:
            hashed_string = bcrypt.generate_password_hash(str(stringToHash)).decode('utf-8')
        else:
            break
        
    return hashed_string


def saveImageFiles(files, folder='covers', resize = False, allowed_formats=['png', 'jpg', 'jpeg', 'bmp']):
    fileNames = []
    for file in files:
        ext = file.filename.split('.')[-1]
        if ext in allowed_formats:
            #fileName = secure_filename(file.filename)
            fileName = secrets.token_hex(16) + '.' + ext
            filePath=os.path.join(current_app.root_path, 'static', 'images', folder, fileName)

            if resize!=False:
                file = Image.open(file)
                file.thumbnail(resize)

            file.save(filePath)
            fileNames.append(fileName)
    return fileNames

def setPostOperation(data):
    operation={}
    if 'coverImage' in data:
        if data['coverImage'] == '_DELETE':
            del data['coverImage']
            operation = {'$set': data,
                        '$unset': {'coverImage': ''}}
        else:
            operation = {'$set': data}
    else:
        operation = {'$set': data}
    
    return operation