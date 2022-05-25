import os
from flask import current_app
from datetime import timedelta

###It is recommended that you save sensitive configuration data as environment variables
##access them using the os module: os.environ.get('NAME_OF_VARIABLE')

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')

    JWT_SECRET_KEY=os.getenv('SECRET_KEY')
    JWT_TOKEN_LOCATION=["cookies"]
    JWT_COOKIE_SECURE=False
    JWT_CSRF_IN_COOKIES=True
    JWT_COOKIE_CSRF_PROTECT =True ###Should be set to True when in production
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=90) ##expiration duration of access tokens

    PASS_RESET_TOKEN_DURATION = '600000' ##expiration duration of password reset token

    MAIL_SENDGRID_API_KEY=os.getenv('MAIL_SENDGRID_API_KEY')
    MAIL_SENDGRID_SENDER=os.getenv('MAIL_SENDGRID_API_KEY') ##validated email for sendgrid sender
    
    MONGO_URI=os.getenv('MONGO_URI')

    """
    Stripe payment test - API keys
    """
    STRIPE_PUBLISHABLE_KEY=os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY=os.getenv('STRIPE_SECRET_KEY')
    STRIPE_ENDPOINT_SECRET=os.getenv('STRIPE_ENDPOINT_SECRET')


