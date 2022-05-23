from flask import request, jsonify, current_app, url_for
from flask_jwt_extended import current_user
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from ..utils.helperFuncs import hashUrlSafe
from ..utils.email import sendEmailToken
from .errorController import AppError
from ..models.userModel import User
from ..utils.helperFuncs import saveImageFiles
from app import bcrypt
from datetime import datetime
import json

###route controllers
def createOne():

    data = User.filterData(request.form.to_dict())

    if request.files:
        data['image']=saveImageFiles(request.files.getlist('image'), folder='users', resize = (150, 200))[0]

    user = User(data)
    ##user.save(pre_hooks=[user.hashpw])
    
    return jsonify({
        'status': 'success',
        'data': [vars(user)],
        'message': 'Registrations are disabled.'
    }), 201


def updateOne(userId):
    user = User.findOne({'_id': userId})
    if user is None:
        return AppError('User not found', 404)
    
    data = User.filterData(request.form.to_dict())
    if(('password' in data) or ('passwordConfirm' in data)):
        return AppError('Please use /changePassword endpoint for changing password', 400)

    if request.files:
        data['image']=saveImageFiles(request.files.getlist('image'), folder='users', resize = (150, 200))[0]

    user.update({'$set': data})
    return jsonify({
        'status': 'success',
        'data': [vars(user)],
        'message': 'Update successfull'
    }), 200

def updatePassword(userId):
    user = User.findOne({'_id': userId})
    if user is None:
        return AppError('User not found.', 404)
    
    data = request.form.to_dict()
    if('currentPassword' not in data) or ('newPassword' not in data) or ('confirmNewPassword' not in data):
        return AppError('Input field missing', 400)


    if not bcrypt.check_password_hash(user.password, data['currentPassword']):
        return AppError('Current password does not match the database', 401)

    user.update({'$set': {'password': data['newPassword'],
                'passwordConfirm': data['confirmNewPassword'],
                'passwordChangedAt': datetime.utcnow().strftime('%Y-%m-%d %H:%M')}},
                pre_hooks=[user.hashpw])

    access_token = create_access_token(identity=user._id)

    response = jsonify({
            'status': 'success',
            'data': None,
            'message': 'Password updated successfully',
            'access_token': access_token
        })
    set_access_cookies(response, access_token)

    return response, 200


def resetPasswordToken():
    data = User.filterData(request.form.to_dict())
    if 'email' not in data: 
        return AppError('Email is a required field', 400)

    user = User.findOne({'email': data['email']})
    if user is None: 
        return AppError('User not found.', 404)

    exp_time = int(datetime.utcnow().timestamp()) + int(current_app.config['PASS_RESET_TOKEN_DURATION'])
    
    reset_token = hashUrlSafe(current_app.config['SECRET_KEY'])
    user.update({'$set': {'passwordResetToken': reset_token,
                        'tokenExpires': exp_time}})

    url = url_for('userRoutes.resetPassword', reset_token=reset_token)
    ####Change the URL string to a valid string once in production (add base url + protocol)
    sendEmailToken(data['email'],
                    'Password reset token',
                    f"Please follow this link to reset your password: {url}")

    return jsonify({
        'status': 'success',
        'data': None,
        'message': f'Password reset token sent to {user.email}'
    }), 200


def resetPassword(reset_token):
    user = User.findOne({'passwordResetToken': reset_token})
    if user is None:
        return AppError('Invalid reset token.', 404)

    if int(user.tokenExpires) < int(datetime.utcnow().timestamp()):
        return AppError('This password reset token expired. Please get a new one!'), 400

    if bcrypt.check_password_hash(reset_token, current_app.config['SECRET_KEY'])==False:
        return AppError('Corrupt password reset URL.', 401)
    
    data = User.filterData(request.form.to_dict())
    if(('password' not in data) or ('passwordConfirm' not in data)):
        return AppError('Missing password or password confirm field.', 400)
    password, passwordConfirm = data['password'], data['passwordConfirm']

    user.update({'$set': {'password': password, 'passwordConfirm': passwordConfirm},
                '$unset': {'passwordResetToken': '',
                            'tokenExpires': ''}}, pre_hooks=[user.hashpw]
                )

    return jsonify({
        'status': 'success',
        'data': None,
        'message': 'Password was reset successfully'
    }), 200

####after request controllers
def removeResponseFields(response, remove_fields):
    try: #tries to filter out unwanted data fields in the response
        data = response.get_json()
        for r in data['data']:
            for key in remove_fields:
                if key in r.keys():
                    del r[key]
        response.data = json.dumps(data)
        return response
    except:
        return response