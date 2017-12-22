"""
Routes and views for the flask application.
"""

from flask import render_template, request, json, jsonify
from LendUpCodingChallenge import app, validate_twilio_request, celery, get_db, BASE_URL
from functools import wraps
from TwilioFizzBuzz import TwilioFizzBuzz
from twilio.rest import Client
from datetime import datetime
import phonenumbers
from helpers import *
import urllib.parse

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home Page'
    )

@app.route('/simple', methods=['GET', 'POST'])
@validate_twilio_request
def simple():
    ''' For Phase 1: Simple TwiML PhoneBuzz '''
    delay = request.args.get("delay")
    return TwilioFizzBuzz.simple(delay)

@app.route('/outbound', methods=['POST'])
def outbound():
    ''' For Phase 2: Dialing PhoneBuzz '''
    rawPhoneNumber = request.form.get('phoneNumber')
    try:
        phoneNumber = convert_to_e164(rawPhoneNumber)
    except phonenumbers.NumberParseException:
        return jsonify(status='BAD', message='Invalid Phone Number!')

    client = TwilioFizzBuzz.outbound(phoneNumber)

    vars = {"delay" : 0}
    try:
        client.calls.create(to=phoneNumber, from_=app.config['TWILIO_NUMBER'], url=BASE_URL+"/simple?"+urllib.parse.urlencode(vars))
    except Exception as e:
        return jsonify(status='BAD', message=str(e))
    
    return jsonify(status='OK')

@app.route('/timed', methods=['POST'])
def timed():
    ''' For Phase 3: Delayed PhoneBuzz '''
    rawPhoneNumber = request.form.get('phoneNumber')
    try:
        phoneNumber = convert_to_e164(rawPhoneNumber)
    except phonenumbers.NumberParseException:
        return jsonify(status='BAD', message='Invalid Phone Number!')

    delay = float(request.form.get('delay')) # Delay in seconds; input validation is done on front end

    client = TwilioFizzBuzz.outbound(phoneNumber)

    callAsync.apply_async(args=[client, phoneNumber, delay], countdown=delay)

    return jsonify(status='OK')

@app.route('/history', methods=['POST'])
def history():
    '''For Phase 4: Tracking PhoneBuzz'''
    db = get_db()
    cur = db.execute('SELECT * FROM history ORDER BY placed DESC')
    entries = cur.fetchall()
    return jsonify(history=entries)

@app.route('/replay', methods=['POST'])
def replay():
    '''For Phase 4: Tracking PhoneBuzz'''
    phoneNumber = request.form.get("phoneNumber")
    n = request.form.get("n")
    logCall(phoneNumber, 0, n)

    client = TwilioFizzBuzz.outbound(phoneNumber)

    vars = {'n' : n}
    try:
        client.calls.create(to=phoneNumber, from_=app.config['TWILIO_NUMBER'], url=BASE_URL+"/replayfizzbuzz?" + urllib.parse.urlencode(vars))
    except Exception as e:
        return jsonify(status='BAD', message=str(e))
    
    return jsonify(status='OK')

@app.route('/replayfizzbuzz', methods=['POST'])
@validate_twilio_request
def replayFizzBuzz():
    n = int(request.args.get("n"))
    return TwilioFizzBuzz.fizzBuzz(n)

@app.route('/fizzbuzz', methods=['GET', 'POST'])
def fizzBuzz():
    ''' For generating FizzBuzz TwiML '''
    delay = request.args.get("delay")
    phoneNumber = request.args.get("Called")
    n = int(request.args.get("Digits"))
    logCall(phoneNumber, delay, n)
    return TwilioFizzBuzz.fizzBuzz(n)
