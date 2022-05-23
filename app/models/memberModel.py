from app import mongo
from xmlrpc.client import Boolean
from .validator import Validator
from .model import Model
from app import bcrypt


class Member(Model):
    session=mongo.db
    collection = 'member'
    __ModelName__ = 'Member'

    Schema = {
        'name': {
            'type': str,
            'validators': [
                (Validator.minLength, 5),
                (Validator.maxLength, 25)
            ],
            'required': True
        },
        'email': {
            'type': str,
            'validators': [
                (Validator.isEmail, True)
            ],
            'required': True
        },
        'education': {
            'type': str,
            'validators': [
                (Validator.minLength, 8)
            ],
            'required': True
        },
        'employment': {
            'type': str,
            'required': True,
            'validators': [
                (Validator.minLength, 4)
            ]
        },
        'shortDescription': {
            'type': str,
            'required': True,
            'validators': [
                (Validator.minLength, 30),
                (Validator.maxLength, 400)
            ]
        },
        'researchInterests': {
            'type': str,
            'required': True,
            'validators': [
                (Validator.minLength, 20),
                (Validator.maxLength, 200)
            ]
        },
        'image': {
            'type': str,
            'required': True,
            'default': 'default.jpg'
        },
        'active': {
            'type': Boolean,
            'required': True,
            'default': True
        },
        'sicris': {
            'type': str,
            'required': False
        },
        'googleScholar': {
            'type': str,
            'required': False
        },
        'linkedin': {
            'type': str,
            'required': False
        },
        'facebook': {
            'type': str,
            'required': False
        },
        'instagram': {
            'type': str,
            'required': False
        }
    }
    
    def __init__(self, data, validate=True, onLoad=False):
        #super().__init__(user)
        Model.__init__(self, data, validate=validate, onLoad=onLoad)
    
    def hashpw(self):
        self.password = bcrypt.generate_password_hash(self.password).decode('utf-8')
        self.passwordConfirm = self.password
        return self