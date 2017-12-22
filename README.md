# PhoneBuzz
LendUp Coding Challenge

Built with Python 3.5 and Flask. I opted to use celery and redis to do the call scheduling.

Required Python Packages:
```
Flask==0.12.2
twilio==6.10.0
phonenumbers==8.8.8
celery==3.1.25
redis==2.10.6
```

config.py requires a Twilio auth token, Twilio account SID, Twilio phone number, a url to redis, and the URL of the environment.

An SQLite database file with an empty table is included, but the database can also be created by running
```
>>> from LendUpCodingChallenge import init_db
>>> init_db()
```

A celery worker needs to be started before the application.
```
celery -A LendUpCodingChallenge.celery worker --loglevel=debug
```

