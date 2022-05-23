from flask import Blueprint
from flask_jwt_extended import jwt_required, current_user
from ..controllers import menuController

menuRoutes = Blueprint('menuRoutes', __name__)

@menuRoutes.route('/api/v1/menu/save', methods=['POST'])
@jwt_required()
def saveMenu():
    return menuController.saveMenu()


@menuRoutes.route('/api/v1/menu/delete', methods=['DELETE'])
@jwt_required()
def deleteMenu():
    return menuController.deleteMenu()


@menuRoutes.route('/api/v1/menu/load', methods=['GET'])
def loadMenu():
    return menuController.loadMenu()