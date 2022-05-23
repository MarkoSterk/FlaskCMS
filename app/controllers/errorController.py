from flask import abort, jsonify, make_response
from werkzeug.exceptions import HTTPException

"""
Error handling controllers.

AppError <- controller for raising/returning predictable app errors

handle_error: overrides the default error responses for all exception codes.
"""

##function for raising exceptions when needed.
def AppError(msg, statusCode):
    response = jsonify({
        'status': 'error',
        'message': msg,
        'code': statusCode
        })
    response = make_response(response)
    return abort(response, statusCode)


###function for exception handling
def handle_error(err):
    code = 500
    if isinstance(err, HTTPException):
        code = err.code
        description = err.description
    
    if code == 500:
        description='An error occured. Please come back later. We are sorry.'

    response = jsonify({
        'status': 'error',
        'message': description,
        'code': code
    })
    response = make_response(response)
    return abort(response, code)