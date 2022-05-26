from app import mongo
from xmlrpc.client import Boolean
from .validator import Validator
from .model import Model
import secrets
from slugify import slugify
from datetime import datetime


class Project(Model):
    session=mongo.db
    collection = 'project'
    __ModelName__ = 'Project'

    Schema = {
        'title': {
            'type': str,
            'validators': [
                (Validator.minLength, 5)
            ],
            'required': True
        },
        'titleSlo': {
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
        'textSlo': {
            'type': str,
            'validators': [
                (Validator.minLength, 10)
            ],
            'required': True
        },
        'projectLeader': {
            'type': str,
            'required': True
        },
        'url': {
            'type': str,
            'required': False,
            'validators': [
                (Validator.minLength, 5)
            ]
        },
        'projectID': {
            'type': str,
            'required': False
        },
        'startDate': {
            'type': str,
            'required': True
        },
        'endDate': {
            'type': str,
            'required': True
        },
        'coverImage': {
            'type': str,
            'required': False
        },
        'tags': {
            'type': list,
            'validators': [
                (Validator.checkElementsType, (str))
            ],
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