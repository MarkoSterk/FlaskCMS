from app import mongo
from xmlrpc.client import Boolean
from .validator import Validator
from .model import Model
import secrets
from slugify import slugify
from datetime import datetime


class Comment(Model):
    session=mongo.db
    collection = 'comment'
    __ModelName__ = 'Comment'

    Schema = {
        'authorName': {
            'type': str,
            'validators': [
                (Validator.minLength, 5)
            ],
            'required': True
        },
        'authorId': {
            'type': str,
            'required': True
        },
        'text': {
            'type': str,
            'validators': [
                (Validator.minLength, 10)
            ],
            'required': True
        },
        'parentId': {
            'type': str,
            'required': True
        },
        'parentCollection': {
            'type': str,
            'required': True,
            'validators': [
                (Validator.inList, ['post', 'project', 'publication'])
            ]
        },
        'active': {
            'type': Boolean,
            'required': True,
            'default': True
        }
    }
    
    def __init__(self, data, validate=True, onLoad=False):
        #super().__init__(user)
        Model.__init__(self, data, validate=validate, onLoad=onLoad)