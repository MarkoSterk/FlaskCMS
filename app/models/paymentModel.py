from app import mongo
from xmlrpc.client import Boolean
from .validator import Validator
from .model import Model
import secrets
from slugify import slugify
from datetime import datetime


class Payment(Model):
    session=mongo.db
    collection = 'payment'
    __ModelName__ = 'Payment'

    Schema = {
        'purchaseId': {
            'type': str,
            'required': True
        },
        'productId': {
            'type': str,
            'required': True
        },
        'client': {
            'type': str,
            'validators': [
                (Validator.isEmail, True)
            ],
            'required': True
        },
        'amountTotal': {
            'type': (int, float),
            'required': True
        },
        'currency': {
            'type': str,
            'required': True
        },
        'status': {
            'type': Boolean,
            'default': True
        }

    }
    
    def __init__(self, data, validate=True, onLoad=False):
        #super().__init__(user)
        Model.__init__(self, data, validate=validate, onLoad=onLoad)