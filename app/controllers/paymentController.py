from flask import request, jsonify, current_app, render_template
from flask_weasyprint import HTML, render_pdf
from importlib_metadata import metadata
from .errorController import AppError
from ..models.paymentModel import Payment
from ..models.productModel import Product
from flask_jwt_extended import current_user
from datetime import datetime
import stripe
from threading import Thread
import sys


def createPayment(data):
    print('Product ID is: ', data['metadata']['productId'])
    product = Product.findOne({'_id': data['metadata']['productId']})
    product.update({'$set': {'quantity': product.quantity-1}})
    payment = Payment({
        'purchaseId': data['id'],
        'productId': data['metadata']['productId'],
        'client': data['customer_email'],
        'amountTotal': data['amount_total']/100.0, ##conversion from cents to $ or €
        'currency': data['currency']
    })

    payment.save()

    # product = Product.findOne({'_id': data['metadata']['productId']})
    # print('Product quantity is: ', product['quantity'])
    # product.update({'$set': {'quantity': product['quantity']-1}})

    sys.exit()



def get_publishable_key():
    stripe_config = {"publicKey": current_app.config["STRIPE_PUBLISHABLE_KEY"]}
    return jsonify(stripe_config)


def create_checkout_session():
    domain_url = "http://localhost:3000"
    stripe.api_key=current_app.config['STRIPE_SECRET_KEY']

    data = request.get_json()

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + 'https://full-flask-cms.herokuapp.com/api/v1/payments/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + 'https://full-flask-cms.herokuapp.com/api/v1/payments/cancelled',
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": data['name'],
                    "quantity": int(data['quantity']),
                    "currency": 'USD',
                    "amount": int(float(data['price'])*100),
                    "images": [
                        'https://images.unsplash.com/photo-1650535812141-04d564530b17?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80'
                    ]
                }
            ],
            customer_email=current_user.email,
            client_reference_id=current_user._id,
            metadata={
                "productId": data['productId']
            }
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return AppError(str(e), 403)


def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, current_app.config["STRIPE_ENDPOINT_SECRET"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        data = event['data']['object']
        Thread(target=createPayment, args=[data]).start()

    return jsonify(success=True)


def downloadPayment(paymentId, populate=False, populateData = {}):
    payment = Payment.findOne({'purchaseId': paymentId})
    if payment is None:
        return AppError(f'Payment with this ID does not exist.', 404)

    if populate:
        payment.populate(populateData)
    
    html = render_template('cms/downloadPayment.html', payment=payment)
    return render_pdf(HTML(string=html))