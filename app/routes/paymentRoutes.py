from flask import Blueprint, jsonify, render_template, request
from flask_jwt_extended import jwt_required


from app.controllers.errorController import AppError
from ..models.productModel import Product
from ..models.paymentModel import Payment
from ..controllers import paymentController
from ..controllers import handlerFactory


paymentRoutes = Blueprint('paymentRoutes', __name__)

@paymentRoutes.route('/api/v1/payments/config', methods=['GET'])
def get_publishable_key():
    return paymentController.get_publishable_key()



@paymentRoutes.route('/api/v1/payments/create-checkout-session', methods=['POST'])
@jwt_required()
def create_checkout_session():
    return paymentController.create_checkout_session()


@paymentRoutes.route("/api/v1/payments/success")
def success():
    return jsonify({
        'status': 'success',
        'message': 'Payment completed successfully',
        'code': 200
    }), 200


@paymentRoutes.route("/api/v1/payments/cancelled")
def cancelled():
    return jsonify({
        'status': 'error',
        'message': 'Payment canceled',
        'code': 200
    }), 200


@paymentRoutes.route("/api/v1/payments/webhook", methods=["POST"])
def stripe_webhook():
    return paymentController.stripe_webhook()

@paymentRoutes.route("/api/v1/payments/<string:paymentId>", methods=["GET"])
@jwt_required()
def getPayment(paymentId):
    return handlerFactory.getOne(paymentId, Payment,
                                populate=True,
                                populateData={
                                    'field': 'productId',
                                    'model': Product,
                                    'hideFields': []
                                })

@paymentRoutes.route('/api/v1/payments/download/<string:paymentId>', methods=['GET'])
@jwt_required()
def downloadPayment(paymentId):
    return paymentController.downloadPayment(paymentId,
                                            populate=True,
                                            populateData={
                                                'field': 'productId',
                                                'model': Product,
                                                'hideFields': []
                                            })
