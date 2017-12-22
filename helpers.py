from LendUpCodingChallenge import get_db, celery, app, BASE_URL
import phonenumbers
from twilio.rest import Client
from datetime import datetime
import urllib.parse

def convert_to_e164(raw_phone):
    if not raw_phone:
        raise phonenumbers.NumberParseException(phonenumbers.NumberParseException.TOO_SHORT_NSN, 'Emtpy number!')

    if raw_phone[0] == '+':
        # Phone number may already be in E.164 format.
        parse_type = None
    else:
        # If no country code information present, assume it's a US number
        parse_type = "US"

    phone_representation = phonenumbers.parse(raw_phone, parse_type)
    return phonenumbers.format_number(phone_representation,
        phonenumbers.PhoneNumberFormat.E164)

def logCall(phoneNumber, delay, n):
    db = get_db()
    db.execute('INSERT INTO history (placed, delay, phoneNumber, n) VALUES (?, ?, ?, ?)', [datetime.now(), delay, phoneNumber, n])
    db.commit()
    return

@celery.task
def callAsync(client, phoneNumber, delay):
    vars = {"delay" : delay}
    client.calls.create(to=phoneNumber,
                            from_=app.config['TWILIO_NUMBER'],
                            url=BASE_URL + "/simple?"+urllib.parse.urlencode(vars))
    return