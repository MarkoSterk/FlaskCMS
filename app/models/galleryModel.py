from app import mongo
from xmlrpc.client import Boolean
from .validator import Validator
from .model import Model
import secrets
from slugify import slugify
from datetime import datetime


class Gallery(Model):
    session=mongo.db
    collection = 'gallery'
    __ModelName__ = 'Gallery'

    Schema = {
        'title': {
            'type': str,
            'validators': [
                (Validator.minLength, 5),
                (Validator.maxLength, 150)
            ],
            'required': True
        },
        'text': {
            'type': str,
            'validators': [
                (Validator.minLength, 10)
            ],
            'required': True
        },
        'images': {
            'type': list,
            'validators': [
                (Validator.checkElementsType, str),
                (Validator.minLength, 1)
            ],
            'required': True
        },
        'coverImage': {
            'type': str,
            'required': True,
            'default': 'default.png'
        },
        'slug': {
            'type': str,
            'required': False
        },
        'active': {
            'type': Boolean,
            'required': True,
            'default': True
        },
        'dateEdited': {
            'type': str,
            'required': False
        },
        'author': {
            'type': str,
            'required': True
        },
        'authorName': {
            'type': str,
            'required': True
        }
    }
    
    def __init__(self, data, validate=True, onLoad=False):
        #super().__init__(user)
        Model.__init__(self, data, validate=validate, onLoad=onLoad)
    
    def slugify(self):
        self.slug = secrets.token_hex(1) + '-' + slugify(getattr(self, 'title'))
        return self