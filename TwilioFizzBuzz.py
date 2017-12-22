from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.request_validator import RequestValidator
from twilio.rest import Client
from LendUpCodingChallenge import app
import urllib.parse

class TwilioFizzBuzz:
    ''' Class for generating FizzBuzz TwiML'''
    GREETING = "Welcome to Shawn's PhoneBuzz Game."
    INPUT_TYPE = 'dtmf'
    INPUT_DIGITS = None # Value of None results in unlimited digits
    INPUT_TIMEOUT = 5
    VOICE_LANGUAGE = 'en'
    VOICE_GENDER = 'man'
  
    '''Return Type: TwilML string'''
    def simple(delay):
        response = VoiceResponse()
        response.say(TwilioFizzBuzz.GREETING, voice=TwilioFizzBuzz.VOICE_GENDER, language=TwilioFizzBuzz.VOICE_LANGUAGE)

        gather = Gather(input = TwilioFizzBuzz.INPUT_TYPE,
                        method = "GET",
                        timeout = TwilioFizzBuzz.INPUT_TIMEOUT, 
                        num_digits = TwilioFizzBuzz.INPUT_DIGITS, 
                        action = '/fizzbuzz?delay=' + delay)
        gather.say('Please enter a number.', voice=TwilioFizzBuzz.VOICE_GENDER, language=TwilioFizzBuzz.VOICE_LANGUAGE)

        response.append(gather)
        response.redirect('/simple') # If user doesn't input anything, restart 

        return str(response)

    ''' Return Type: twilio Client '''
    def outbound(phoneNumber: str):
        account_sid = app.config['TWILIO_ACC_SID']
        auth_token = app.config['TWILIO_AUTH_TOKEN']

        client = Client(account_sid, auth_token)
        return client

    '''Return Type: TwilML string'''
    def fizzBuzz(n: int):
        output = [] # Use list to avoid string concatenation
        i = 1
        for i in range(1, n+1):
            if i % 3 == 0 and i % 5 == 0:
                output.append("FizzBuzz")
            elif i % 3 == 0:
                output.append("Fizz")
            elif i % 5 == 0:
                output.append("Buzz")
            else:
                output.append(str(i))

        outputStr = ' '.join(output)
        response = VoiceResponse()
        response.say(outputStr, voice=TwilioFizzBuzz.VOICE_GENDER, language=TwilioFizzBuzz.VOICE_LANGUAGE)
        return str(response)

class CallRecord():
    def __init__(self, placed, number, delay, n):
        self.placed = placed
        self.number - number
        self.delay = delay
        self.n = n