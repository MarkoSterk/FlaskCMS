from app import mongo
from xmlrpc.client import Boolean
from .validator import Validator
from .model import Model
import secrets
from slugify import slugify
from datetime import datetime


class Product(Model):
    session=mongo.db
    collection = 'product'
    __ModelName__ = 'Product'

    Schema = {
        'name': {
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
        'price': {
            'type': (int, float),
            'required': True,
            'validators': [
                (Validator.minValue, 0.00)
            ]
        },
        'quantity': {
            'type': (int, float),
            'required': True,
            'validators': [
                (Validator.minValue, 0)
            ]
        },
        'images': {
            'type': list,
            'validators': [
                (Validator.checkElementsType, str),
            ],
            'required': True,
            'default': ['default.jpg']
        },
        'slug': {
            'type': str,
            'required': False
        },
        'author': {
            'type': str,
            'required': True
        },
        'dateEdited': {
            'type': str,
            'required': False
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
    
    def slugify(self):
        self.slug = secrets.token_hex(1) + '-' + slugify(getattr(self, 'name'))
        return self