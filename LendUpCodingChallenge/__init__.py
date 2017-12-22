"""
The flask application package.
"""

from flask import Flask, abort, request, g
from functools import wraps
from twilio.request_validator import RequestValidator
from celery import Celery
import sqlite3
import os

from celery import current_app
from celery.bin import worker

app = Flask(__name__)
app.config.from_object('config')

BASE_URL = app.config['BASE_URL']

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

def connect_db():
    return sqlite3.connect('history.db')

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validator = RequestValidator(app.config['TWILIO_AUTH_TOKEN'])
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function

import LendUpCodingChallenge.views
