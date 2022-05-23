from app import mongo
from xmlrpc.client import Boolean
from .validator import Validator
from .model import Model
import secrets
from slugify import slugify
from datetime import datetime


class Publication(Model):
    session=mongo.db
    collection = 'publication'
    __ModelName__ = 'Publication'

    Schema = {
        'title': {
            'type': str,
            'validators': [
                (Validator.minLength, 5)
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
        'journal': {
            'type': str,
            'validators': [
                (Validator.minLength, 5)
            ],
            'required': True
        },
        'authors': {
            'type': list,
            'validators': [
                (Validator.checkElementsType, str)
            ],
            'required': True
        },
        'doi': {
            'type': str,
            'required': False,
            'validators': [
                (Validator.minLength, 5)
            ]
        },
        'coverImage': {
            'type': str,
            'required': False
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