from flask import jsonify, request, current_app
from flask_jwt_extended import current_user

import os
import json
from datetime import datetime

from .errorController import AppError


#####Menu structure paths
def menuPaths():
    DEFAULT_MENU=os.path.join(current_app.root_path, 'static', 'menu', 'defaultMenu.json')
    CUSTOM_MENU=os.path.join(current_app.root_path, 'static', 'menu', 'customMenu.json')
    return DEFAULT_MENU, CUSTOM_MENU


def saveMenu():
    if current_user.role!='admin':
        return AppError('Only Admins can change the menu.', 401)
    
    DEFAULT_MENU, CUSTOM_MENU = menuPaths()

    structure = request.get_json()
    
    menu = {}
    menu['name']='custom'
    menu['dateChanged'] = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
    menu['userId']=current_user._id
    menu['structure']=structure

    
    
    status='success'
    msg='Menu saved successfully.'
    statusCode=200
    try:
        with open(CUSTOM_MENU, "w") as outfile:
            outfile.write(json.dumps(menu, indent = 4))
    
    except IOError:
        status='error'
        msg='Failed to save menu.'
        statusCode=500


    return jsonify({
        'status': status,
        'data': None,
        'message': msg
    }), statusCode


def deleteMenu():

    if current_user.role!='admin':
        return AppError('Only Admins can delete the menu.', 401)

    status='success'
    msg='Menu deleted successfully.'
    statusCode=204

    DEFAULT_MENU, CUSTOM_MENU = menuPaths()
    
    if os.path.exists(CUSTOM_MENU):
        try:
            os.remove(CUSTOM_MENU)
        except IOError:
            status='error'
            msg='Failed to delete menu'
            statusCode=500
    else:
        status='error'
        msg='Menu does not exist'
        statusCode=400

    return jsonify({
        'status': status,
        'data': None,
        'message': msg
    }), statusCode


def loadMenu():
    status='success'
    msg='Menu loaded successfully'
    statusCode=200

    DEFAULT_MENU, CUSTOM_MENU = menuPaths()

    try:
        if os.path.exists(CUSTOM_MENU):
            menu=json.load(open(CUSTOM_MENU))
        else:
            menu=json.load(open(DEFAULT_MENU))
    except IOError:
        menu=None
        status='error'
        msg='Failed to load menu'
        statusCode=500
    
    return jsonify({
        'status': status,
        'data': menu,
        'message': msg
    }), statusCode