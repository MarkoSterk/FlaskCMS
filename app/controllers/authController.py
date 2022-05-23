from flask import jsonify, request, Response
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask_jwt_extended import current_user
from flask_jwt_extended import unset_jwt_cookies, unset_access_cookies
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity

from ..models.userModel import User
from .errorController import AppError
from app import jwt, bcrypt


def login():
    data = request.form.to_dict()
    if (('email' not in data) or ('password' not in data)):
        return AppError('Missing input fields!', 400)

    user = User.findOne({'email': data['email']})

    if user is None or bcrypt.check_password_hash(user.password, data['password'])==False:
        return AppError('Wrong email or password.', 400)
    
    msg = f'User {user.name} logged in successfully.'
    access_token = create_access_token(identity=user._id)

    response = jsonify({
            'status': 'success',
            'data': None,
            'message': msg,
            'access_token': access_token
        })
    set_access_cookies(response, access_token)
    return response, 200


def logout():
    
    response = jsonify({
        'status': 'success',
        'data': None,
        'message': 'logout successful'
        })
    unset_jwt_cookies(response)
    unset_access_cookies(response)
    return response


@jwt.expired_token_loader
def mexpiredTokenCallback(jwt_header, jwt_payload):
    return jsonify({
        'status': 'error',
        'message': 'Your access token has expired. Please login again',
        'code': 401
    }), 401


def refreshExpiringJWTS(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=60))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.invalid_token_loader
def invalid_token_callback(string):
    return Response('Corrupt verification token/cookie', 401)


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return Response('Missing verification token/cookie. Please login.', 401)


@jwt.token_verification_failed_loader
def token_verification_failed_callback(_jwt_header, jwt_data):
    return Response('Verification failed. Please renew your access token/cookie by loging in again.', 401)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    iat = jwt_data['iat']
    user = User.findOne({'_id': identity, 'active': True})
    passwordChangedAt = 0
    if 'passwordChangedAt' in vars(user):
        passwordChangedAt = int(datetime.strptime(user.passwordChangedAt, "%Y-%m-%d %H:%M").strftime("%s"))
    
    if iat<passwordChangedAt: 
        return AppError('You recently changed your password. Please sign in again', 401)
    
    return user

###decorator function
###access restriction to user roles
def role_required(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user['role'] not in access_level:
                return AppError(f'You do not have the required access level', 401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator